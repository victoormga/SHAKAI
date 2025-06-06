from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Follow
from users.models import User
from notifications.models import Notification
from django.core.exceptions import PermissionDenied

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
    # Comprobar si ya existe el follow o solicitud pendiente
    existing = Follow.objects.filter(follower=request.user, following=target).first()
    if existing:
        return Response({"detail": "Ya existe esta relación o solicitud."}, status=status.HTTP_400_BAD_REQUEST)

    # Si target es privado, is_accepted=False, si es público, se acepta automáticamente
    is_accepted = not target.profile.is_private
    follow_obj = Follow.objects.create(follower=request.user, following=target, is_accepted=is_accepted)

    if target.profile.is_private:
        # 1) Emitir notificación de “solicitud de seguimiento”
        Notification.objects.create(
            recipient=target,
            sender=request.user,
            notif_type="follow_request"
        )
        return Response({"detail": "Solicitud de seguimiento enviada."}, status=status.HTTP_201_CREATED)
    else:
        # 2) Usuario público: auto-acepta y notifica inmediatamente
        Notification.objects.create(
            recipient=target,
            sender=request.user,
            notif_type="follow_accepted"
        )
        return Response({"detail": "Ahora sigues a este usuario."}, status=status.HTTP_201_CREATED)

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_follow_request(request, follow_id):
    """
    Endpoint para que el dueño del perfil acepte una solicitud pendiente.
    URL: POST /api/follow/accept/<follow_id>/
    """
    follow_obj = get_object_or_404(Follow, id=follow_id)

    # Solo quien recibe la solicitud (following) puede aceptarla
    if follow_obj.following != request.user:
        raise PermissionDenied("No puedes aceptar esta solicitud.")

    # Debe estar pendiente (is_accepted=False)
    if follow_obj.is_accepted:
        return Response({"detail": "Esta solicitud ya fue aceptada."}, status=status.HTTP_400_BAD_REQUEST)

    # Aceptar la solicitud
    follow_obj.is_accepted = True
    follow_obj.save()

    # 1) Notificar al que solicitó que ya fue aceptado
    Notification.objects.create(
        recipient=follow_obj.follower,
        sender=request.user,
        notif_type="follow_accepted"
    )

    return Response({"detail": "Solicitud aceptada. Ahora sigues a este usuario."}, status=status.HTTP_200_OK)