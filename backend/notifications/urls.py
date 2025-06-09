from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    # Lista de notificaciones
    path("", NotificationListView.as_view(), name="notif-list"),
    # Marcar una notificación como leída
    path("<int:id>/read/", NotificationMarkReadView.as_view(), name="notif-read"),
]