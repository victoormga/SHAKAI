from django.urls import path
from .views import follow_user, unfollow_user, check_follow_status, accept_follow_request

urlpatterns = [
    path("<int:user_id>/", follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", unfollow_user, name="unfollow-user"),
    path("status/<int:user_id>/", check_follow_status, name="follow-status"),
    path("accept/<int:follow_id>/", accept_follow_request, name="follow-accept"),
]