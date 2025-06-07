# search/views.py

from rest_framework import generics, permissions, filters
from django.db.models import Q

from users.models import Profile
from users.serializers import ProfileListSerializer
from blocks.models import Block

class UserSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["display_name"]

    def get_queryset(self):
        user = self.request.user
        q = self.request.query_params.get("search", "")

        # Bloqueos (tanto yo bloqueé a X como X me bloqueó)
        blocked_pairs = Block.objects.filter(
            Q(blocker=user) | Q(blocked=user)
        ).values_list("blocker_id", "blocked_id")
        blocked_ids = {i for pair in blocked_pairs for i in pair}

        # Buscar perfiles por display_name y excluir bloqueados
        qs = Profile.objects.filter(display_name__icontains=q)

        if blocked_ids:
            qs = qs.exclude(user__id__in=blocked_ids)

        return qs
