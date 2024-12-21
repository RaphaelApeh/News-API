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
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['user', 'title', 'image', 'tags', 'likes', 'slug','comments', 'timestamp']