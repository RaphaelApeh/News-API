from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["user__username", "title", "timestamp", "active"]
    search_fields = ["user__username", "title"]
    list_filter = ["user__username", "active"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin): ...
