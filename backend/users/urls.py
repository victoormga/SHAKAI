from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    LogoutView,
    MyProfileView,
    ProfileDetailView,
    UserSearchView,
    MeView,
)

urlpatterns = [
    # Registro y login
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Mis datos / perfil
    path("me/", MeView.as_view(), name="me"),
    path("me/profile/", MyProfileView.as_view(), name="my-profile"),
    # Perfil de otro usuario
    path("profiles/<int:user_id>/", ProfileDetailView.as_view(), name="profile-detail"),
    # Búsqueda de usuarios
    path("profiles/search/", UserSearchView.as_view(), name="profile-search"),
]