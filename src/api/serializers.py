from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        models = Comment
        fields = ['user', 'text', 'timestamp']


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user = serializers.CharField(source='get_user_display_name')
    tags = TagListSerializerField()
    
    class Meta:
        model = Post
        fields = ['user', 'title', 'tags', 'slug', 'timestamp']