from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

# --------------------------------------------
# Vista para crear una publicación
# --------------------------------------------
class CreatePostView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

# --------------------------------------------
# Vista para listar todas las publicaciones públicas
# (por simplicidad, listamos is_deleted=False)
# --------------------------------------------
class ListPublicPostsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Filtrar posts no borrados
        return Post.objects.filter(is_deleted=False).order_by("-created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

# --------------------------------------------
# Vista para listar todas las publicaciones de un usuario
# --------------------------------------------
class ListUserPostsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Post.objects.filter(user__id=user_id, is_deleted=False).order_by("-created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

# --------------------------------------------
# Vista detalle de un post (GET)
# --------------------------------------------
class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

# --------------------------------------------
# Vista para editar un post (solo autor)
# --------------------------------------------
class EditPostView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise permissions.PermissionDenied("No puedes editar este post")
        serializer.save()

# --------------------------------------------
# Vista para “borrar” (soft delete) un post
# --------------------------------------------
class DeletePostView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        return Post.objects.all()

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"detail": "No tienes permiso para eliminar este post."}, status=status.HTTP_403_FORBIDDEN)
        post.is_deleted = True
        post.save()
        return Response({"detail": "Publicación eliminada."}, status=status.HTTP_204_NO_CONTENT)
