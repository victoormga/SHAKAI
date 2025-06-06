from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile

# --------------------------------------------
# Serializador para registro de usuarios
# --------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "password", "display_name")

    def validate_display_name(self, value):
        if Profile.objects.filter(display_name__iexact=value).exists():
            raise serializers.ValidationError("El display_name ya existe")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        display_name = validated_data["display_name"]

        user = User.objects.create_user(email=email, password=password)
        # El Profile ya se crea automáticamente por la señal, pero queremos actualizar display_name
        profile = user.profile
        profile.display_name = display_name
        profile.save()
        return user

# --------------------------------------------
# Serializador para Login (devuelve tokens)
# --------------------------------------------
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

# --------------------------------------------
# Serializador para ver/modificar el propio perfil
# --------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "email",
            "display_name",
            "bio",
            "profile_image",
            "is_private",
            "created_at",
        )
        read_only_fields = ("created_at", "email")

    def validate_display_name(self, value):
        user = self.context["request"].user
        qs = Profile.objects.filter(display_name__iexact=value).exclude(user=user)
        if qs.exists():
            raise serializers.ValidationError("Este display_name ya está en uso.")
        return value

# --------------------------------------------
# Serializador para exponer datos del usuario (me mismo)
# --------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "profile",)


# --------------------------------------------
# Serializador para lista de perfiles (búsqueda pública)
# --------------------------------------------
class ProfileListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("user", "email", "display_name", "profile_image", "is_private")
        read_only_fields = ("user", "email", "profile_image", "is_private")