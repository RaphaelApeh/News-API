from django.contrib import admin

from .models import Post, Comment

class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
