from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Devuelve las últimas 50 notificaciones del usuario autenticado
        return Notification.objects.filter(recipient=self.request.user)[:50]

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    queryset = Notification.objects.all()
    http_method_names = ["post", "patch", "put", "options", "head"]

    def get_object(self):
        notif = super().get_object()
        if notif.recipient != self.request.user:
            raise PermissionDenied("No puedes modificar esta notificación.")
        return notif

    def post(self, request, *args, **kwargs):
        # Alias para que POST llame a update()
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        serializer = self.get_serializer(notif)
        return Response(serializer.data)