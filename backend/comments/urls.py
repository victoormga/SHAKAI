from django.urls import path
from .views import ListCreateCommentView, CommentDetailView

urlpatterns = [
    path("post/<int:post_id>/comments/", ListCreateCommentView.as_view(), name="comment-list-create"),
    path("comments/<int:comment_id>/", CommentDetailView.as_view(), name="comment-detail"),
]