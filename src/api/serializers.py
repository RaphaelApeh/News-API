import datetime

from django.conf import settings

from rest_framework import serializers

from taggit.serializers import TaggitSerializer, TagListSerializerField

from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'timestamp']

    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username
    

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = serializers.CharField(source='get_user_display_name')
    tags = TagListSerializerField()
    likes = serializers.IntegerField(source='likes_count')
    image = serializers.URLField(source='image_url')
    timestamp = serializers.DateTimeField(source='get_timestamp_format')
    comments = CommentSerializer(many=True)
    detail_url = serializers.SerializerMethodField() 

    class Meta:
        model = Post
        fields = ['user', 'title', 'text', 'image', 'tags', 'likes', 'slug', 'detail_url', 'comments', 'timestamp']

    def get_detail_url(self, obj):
        
        return settings.URL + obj.get_absolute_url()