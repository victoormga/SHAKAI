from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer

# --------------------------------------------
# Vista para listar/crear comentarios de un post
# --------------------------------------------
class ListCreateCommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post__id=post_id, is_deleted=False).order_by("created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        # Pasamos el objeto Post completo al serializer.create()
        from posts.models import Post
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        ctx["post"] = post
        return ctx

# --------------------------------------------
# Vista para obtener / editar / eliminar un comentario
# --------------------------------------------
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

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise permissions.PermissionDenied("No puedes editar este comentario")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("No puedes eliminar este comentario")
        instance.is_deleted = True
        instance.save()