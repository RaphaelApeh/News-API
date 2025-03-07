from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.text import slugify, Truncator

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

    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "content", "timestamp"]
        extra_kwargs = {
            "timestamp": {"required": False}
        }    
    
    def get_timestamp(self, obj):
        return  obj.timestamp.strftime("%d-%m-%Y")

class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    truncated_content = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "user", "title", "slug", "content", "status", "comments", "active", "truncated_content", "image", "detail_url", "timestamp"]

    def get_detail_url(self, obj):
        request = self.context["request"]
        post_detail_url = request.build_absolute_uri(reverse("posts-detail", kwargs={"slug": obj.slug}))
        return post_detail_url
    
    def get_timestamp(self, obj: Post):
        
        return obj.timestamp.strftime("%c")
    
    def get_comments(self, obj):
        request = self.context["request"]
        query = int(request.query_params.get("comment_limits", 2))
        qs = obj.posts.all()[:query]
        return CommentSerializer(qs, many=True, read_only=True).data

    def get_truncated_content(self, obj):

        return Truncator(obj.content).words(20)

    def create(self, validated_data):
        
        user = self.context["request"].user
        return Post.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        
        with transaction.atomic():
            for key, value in validated_data.items():
                setattr(instance, key, value)
                if key == "title":
                    instance.slug = slugify(value)
                instance.save()
        return instance