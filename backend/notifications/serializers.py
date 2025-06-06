from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender_display_name = serializers.CharField(source="sender.profile.display_name", read_only=True)
    recipient_id = serializers.IntegerField(source="recipient.id", read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    comment_id = serializers.IntegerField(source="comment.id", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "sender_display_name",
            "recipient_id",
            "notif_type",
            "post_id",
            "comment_id",
            "created_at",
            "is_read",
        ]