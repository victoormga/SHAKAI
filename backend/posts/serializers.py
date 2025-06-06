from rest_framework import serializers
from .models import Post
from likes.models import Like
from comments.models import Comment

class PostSerializer(serializers.ModelSerializer):
    user_display_name = serializers.CharField(source="user.profile.display_name", read_only=True)
    file_url = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "user_display_name",
            "caption",
            "file",
            "file_url",
            "created_at",
            "is_deleted",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "is_deleted",
            "user_display_name",
            "file_url",
            "likes_count",
            "comments_count",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj, is_deleted=False).count()

    def create(self, validated_data):
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)