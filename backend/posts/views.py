from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer

# Imports para filtrado de feed
from follows.models import Follow
from users.models import Profile
from blocks.models import Block

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
# Vista para listar publicaciones en el feed
# Sólo posts propios, de seguidos o de perfiles públicos,
# excluyendo autores bloqueados
# --------------------------------------------
class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        # 1) IDs de quienes sigo y me aceptaron
        following_ids = Follow.objects.filter(
            follower=user,
            is_accepted=True
        ).values_list("following__id", flat=True)
        # 2) IDs de todos los perfiles públicos
        public_ids = Profile.objects.filter(
            is_private=False
        ).values_list("user__id", flat=True)
        # 3) IDs de bloqueos recíprocos o unidireccionales
        blocked_pairs = Block.objects.filter(
            Q(blocker=user) | Q(blocked=user)
        ).values_list("blocker_id", "blocked_id")
        blocked_ids = {i for pair in blocked_pairs for i in pair}

        # 4) Filtrar posts: propios OR de seguidos OR de públicos
        qs = Post.objects.filter(
            Q(user=user) |
            Q(user__id__in=following_ids) |
            Q(user__id__in=public_ids),
            is_deleted=False
        )
        # 5) Excluir los de bloqueados
        if blocked_ids:
            qs = qs.exclude(user__id__in=blocked_ids)

        return qs.order_by("-created_at")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

# --------------------------------------------
# Vista para listar todas las publicaciones de un usuario
# (se respeta privacidad y bloqueo en otro endpoint)
# --------------------------------------------
class ListUserPostsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        me = self.request.user
        target_id = self.kwargs["user_id"]
        
        from users.models import Profile
        from follows.models import Follow
        from blocks.models import Block

        # 1) Si bloqueado recíproco, no ver nada
        if Block.objects.filter(
            Q(blocker=me, blocked__id=target_id) |
            Q(blocked=me, blocker__id=target_id)
        ).exists():
            return Post.objects.none()

        profile = get_object_or_404(Profile, user__id=target_id)

        # 2) Mostrar posts solo si:
        #    a) soy yo, o 
        #    b) perfil es público, o
        #    c) sigo al usuario y me aceptaron.
        follows = Follow.objects.filter(
            follower=me, following__id=target_id, is_accepted=True
        ).exists()
        if target_id == me.id or not profile.is_private or follows:
            return Post.objects.filter(
                user__id=target_id, is_deleted=False
            ).order_by("-created_at")

        # 3) En cualquier otro caso (perfil privado sin seguir) no devolvemos posts
        return Post.objects.none()

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
            return Response({"detail": "No tienes permiso para eliminar este post."},
                            status=status.HTTP_403_FORBIDDEN)
        post.is_deleted = True
        post.save()
        return Response({"detail": "Publicación eliminada."}, status=status.HTTP_204_NO_CONTENT)
