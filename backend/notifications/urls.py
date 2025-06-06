from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    path(" ", NotificationListView.as_view(), name="notif-list"),
    path("<int:id>/read/", NotificationMarkReadView.as_view(), name="notif-read"),
]