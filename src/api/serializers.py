import datetime

from django.conf import settings
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from taggit.serializers import TaggitSerializer, TagListSerializerField

from posts.models import Post, Comment


User = get_user_model()


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
    timestamp = serializers.DateTimeField(source='get_timestamp_format')
    comments = CommentSerializer(many=True)
    images = serializers.URLField(source='image_url')
    detail_url = serializers.SerializerMethodField() 
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'text', 'image', 'images', 'tags', 'likes', 'slug', 'detail_url', 'comments', 'is_liked', 'timestamp']

    def get_detail_url(self, obj):
        
        return settings.URL + obj.get_absolute_url()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        req_user = request.user
        return obj.likes.contains(req_user)

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        super().__init__(*args, **kwargs)
        if context.get('exclude', []):
            for field_name in context['exclude']:
                self.fields.pop(field_name, None)


class UserSerializer(serializers.ModelSerializer):

    post_set = PostSerializer(many=True)
    num_of_posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'post_set', 'num_of_posts']
    
    def get_num_of_posts(self, obj):
        return obj.post_set.count()
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.get('password')
        validate_password(password) # raise ValidationError
        return User.objects.create_user(**validated_data)