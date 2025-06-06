from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Block
from users.models import User

# --------------------------------------------
# Bloquear a un usuario
# POST /api/block/<user_id>/
# --------------------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def block_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return Response({"detail": "No puedes bloquearte a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)
    existing = Block.objects.filter(blocker=request.user, blocked=target).first()
    if existing:
        return Response({"detail": "Ya has bloqueado a este usuario."}, status=status.HTTP_400_BAD_REQUEST)
    # Si hay solicitud de follow pendiente, la eliminamos
    from follows.models import Follow
    Follow.objects.filter(follower=request.user, following=target).delete()
    Follow.objects.filter(follower=target, following=request.user).delete()

    Block.objects.create(blocker=request.user, blocked=target)
    return Response({"detail": "Usuario bloqueado."}, status=status.HTTP_201_CREATED)

# --------------------------------------------
# Desbloquear a un usuario
# DELETE /api/unblock/<user_id>/
# --------------------------------------------
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unblock_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    block = Block.objects.filter(blocker=request.user, blocked=target).first()
    if not block:
        return Response({"detail": "Este usuario no estaba bloqueado."}, status=status.HTTP_400_BAD_REQUEST)
    block.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)