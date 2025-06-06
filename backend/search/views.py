from rest_framework import generics, permissions, filters
from users.models import Profile
from users.serializers import ProfileListSerializer

class UserSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["display_name"]

    def get_queryset(self):
        return Profile.objects.all()