from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile
from follows.models import Follow
from posts.models import Post
from blocks.models import Block

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
    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "email",
            "display_name",
            "bio",
            "profile_image",
            "is_private",
            "created_at",
            "followers_count",
            "following_count",
            "posts_count",
        )
        read_only_fields = ("created_at", "email")

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj.user, is_accepted=True).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user, is_accepted=True).count()

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj.user, is_deleted=False).count()

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
    is_blocked = serializers.SerializerMethodField()
    is_private = serializers.BooleanField(read_only=True)

    class Meta:
        model = Profile
        fields = ("user", "email", "display_name", "profile_image", "is_private", "is_blocked")
        read_only_fields = ("user", "email", "profile_image", "is_private")

    def get_is_blocked(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Block.objects.filter(blocker=request.user, blocked=obj.user).exists()