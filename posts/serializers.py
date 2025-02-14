from django.contrib.auth import get_user_model

from rest_framework import serializers

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

    class Meta:
        model = Post
        fields = ["user", "title", "content", "status", "comments", "active", "timestamp"]

    def create(self, validated_data):
        
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)