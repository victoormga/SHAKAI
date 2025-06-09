# comments/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer

# Importa Notification
from notifications.models import Notification
from posts.models import Post

class ListCreateCommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post__id=post_id, is_deleted=False).order_by("created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        ctx["post"] = post
        return ctx

    def perform_create(self, serializer):
        # Aquí serializer.create() depende de tu CommentSerializer,
        # pero suponemos que el serializer usa ctx["post"] y request.user.
        comment = serializer.save()
        # Una vez creado el comentario, generamos la notificación:
        Notification.objects.create(
            recipient=comment.post.user,
            sender=self.request.user,
            notif_type="comment",
            post=comment.post,
            comment=comment
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("No puedes eliminar este comentario")
        instance.is_deleted = True
        instance.save()
