# ============================================
# Importaciones necesarias para personalizar el modelo de usuario
# ============================================
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# ============================================
# MANAGER PERSONALIZADO PARA EL MODELO DE USUARIO
# ============================================
class CustomUserManager(BaseUserManager):
    # Método para crear usuarios normales
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # Método para crear superuser (admin)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(email, password, **extra_fields)

# ============================================
# MODELO DE USUARIO PERSONALIZADO
# ============================================
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# ============================================
# PERFIL ASOCIADO AL USUARIO
# ============================================
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    display_name = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    is_private = models.BooleanField(default=False)  # <- Por defecto público (False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

# ============================================
# Señal para crear Profile al crear User
# ============================================
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, display_name=instance.email.split('@')[0])
    else:
        instance.profile.save()