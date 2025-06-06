from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at')
    search_fields = ('caption', 'user__email')
    list_filter = ('created_at',)
