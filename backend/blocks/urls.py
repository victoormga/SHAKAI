from django.urls import path
from .views import block_user, unblock_user

urlpatterns = [
    path("<int:user_id>/", block_user, name="block-user"),
    path("unblock/<int:user_id>/", unblock_user, name="unblock-user"),
]