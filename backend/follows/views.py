from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Follow
from users.models import User

# --------------------------------------------
# Seguir a un usuario
# POST /api/follow/<user_id>/
# --------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return Response({"detail": "No puedes seguirte a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)
    # Comprobar si ya existe el follow
    existing = Follow.objects.filter(follower=request.user, following=target).first()
    if existing:
        return Response({"detail": "Ya existe esta relación."}, status=status.HTTP_400_BAD_REQUEST)

    # Si target es privado, is_accepted=False, si es público, se acepta automáticamente
    is_accepted = not target.profile.is_private
    Follow.objects.create(follower=request.user, following=target, is_accepted=is_accepted)
    return Response({"detail": "Solicitud de seguimiento enviada."}, status=status.HTTP_201_CREATED)

# --------------------------------------------
# Dejar de seguir (o cancelar solicitud pendiente)
# DELETE /api/unfollow/<user_id>/
# --------------------------------------------
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, following=target).first()
    if not follow:
        return Response({"detail": "No estabas siguiendo a este usuario."}, status=status.HTTP_400_BAD_REQUEST)
    follow.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------------
# Comprobar estado de seguimiento
# GET /api/follow/status/<user_id>/
# --------------------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_follow_status(request, user_id):
    is_following = Follow.objects.filter(
        follower=request.user,
        following__id=user_id,
        is_accepted=True
    ).exists()
    return Response({"is_following": is_following})