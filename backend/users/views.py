from rest_framework import generics, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User, Profile
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ProfileSerializer,
    UserSerializer,
    ProfileListSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# --------------------------------------------
# Vista para registrar usuario
# --------------------------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# --------------------------------------------
# Vistas JWT (Login / Refresh)
# --------------------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RefreshTokenView(TokenRefreshView):
    pass

# --------------------------------------------
# Vista para cerrar sesión (blacklist del refresh token)
# --------------------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Sesión cerrada correctamente"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------
# Vista para ver y editar mi propio perfil
# --------------------------------------------
class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# --------------------------------------------
# Vista para ver el perfil de otro usuario (si es público o ya me sigue)
# --------------------------------------------
class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs["user_id"]
        perfil = get_object_or_404(Profile, user__id=user_id)
        # Si el perfil es privado, solo dejo ver si existe Follow con is_accepted=True
        if perfil.is_private:
            from follows.models import Follow
            # Comprobar si el request.user sigue a este usuario y está aceptado
            autorizado = Follow.objects.filter(
                follower=self.request.user,
                following=perfil.user,
                is_accepted=True
            ).exists()
            if not autorizado:
                raise Response({"detail": "Perfil privado"}, status=status.HTTP_403_FORBIDDEN)
        return perfil

# --------------------------------------------
# Vista para obtener mis datos de usuario (incluye perfil)
# --------------------------------------------
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

# --------------------------------------------
# Vista para búsqueda de usuarios (por display_name)
# --------------------------------------------
class UserSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["display_name"]

    def get_queryset(self):
        return Profile.objects.all()

# --------------------------------------------
# Vista para listar todos los perfiles (solo admin, si lo deseas)
# por defecto aquí devolvemos todos; si quieres restringir,
# añade IsAdminUser a permission_classes.
# --------------------------------------------
class ProfileListAllView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProfileListSerializer
    queryset = Profile.objects.all()