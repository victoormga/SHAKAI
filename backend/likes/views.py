# likes/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Like
from posts.models import Post

# Importa Notification
from notifications.models import Notification

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ToggleLikeView(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_deleted=False)
    if post.user == request.user:
        return Response({"detail": "No puedes darte like a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)

    from blocks.models import Block
    if Block.objects.filter(blocker=post.user, blocked=request.user).exists() or \
       Block.objects.filter(blocker=request.user, blocked=post.user).exists():
        return Response({"detail": "No puedes interactuar con este usuario."}, status=status.HTTP_403_FORBIDDEN)

    like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like_obj.delete()
        return Response({"liked": False}, status=status.HTTP_200_OK)

    # Si acabamos de dar like, creamos notificación:
    Notification.objects.create(
        recipient=post.user,
        sender=request.user,
        notif_type="like",
        post=post
    )
    return Response({"liked": True}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def HasLikedView(request, post_id):
    exists = Like.objects.filter(user=request.user, post__id=post_id).exists()
    return Response({"has_liked": exists})
