from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    NOTIF_TYPES = (
        ("follow_request", "Follow Request"),
        ("follow_accepted", "Follow Accepted"),
        ("like", "Like"),
        ("comment", "Comment"),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} → {self.recipient} ({self.notif_type})"