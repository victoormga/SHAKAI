from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user_display_name = serializers.CharField(
        source="user.profile.display_name",
        read_only=True
    )
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "user_display_name",
            "post",
            "content",
            "parent",
            "created_at",
            "is_deleted",
        ]
        read_only_fields = ["user", "created_at", "is_deleted", "user_display_name", "post"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = self.context["post"]
        parent = validated_data.get("parent", None)
        comment = Comment.objects.create(
            user=user,
            post=post,
            content=validated_data["content"],
            parent=parent
        )
        return comment