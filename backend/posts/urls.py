from django.urls import path
from .views import (
    CreatePostView,
    FeedView,
    ListUserPostsView,
    PostDetailView,
    EditPostView,
    DeletePostView,
)

urlpatterns = [
    path("create/", CreatePostView.as_view(), name="post-create"),
    path("feed/", FeedView.as_view(), name="post-feed"),
    path("user/<int:user_id>/", ListUserPostsView.as_view(), name="post-list-user"),
    path("<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/edit/", EditPostView.as_view(), name="post-edit"),
    path("<int:post_id>/delete/", DeletePostView.as_view(), name="post-delete"),
]