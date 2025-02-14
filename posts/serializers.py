from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Post, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "get_full_name"]


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "content", "timestamp"]
    

class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    comments = CommentSerializer(source="posts", many=True, read_only=True)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["user", "title", "slug", "content", "status", "comments", "active", "timestamp"]

    def get_slug(self, obj):
        request = self.context["request"]
        post_detail_url = request.build_absolute_uri(reverse("posts-detail", kwargs={"slug": obj.slug}))
        return post_detail_url

    def create(self, validated_data):
        
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)