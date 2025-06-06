from django.urls import path
from .views import ToggleLikeView, HasLikedView

urlpatterns = [
    path("toggle/<int:post_id>/", ToggleLikeView, name="like-toggle"),
    path("has-liked/<int:post_id>/", HasLikedView, name="like-has-liked"),
]