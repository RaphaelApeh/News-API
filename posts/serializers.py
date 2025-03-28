from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.text import slugify, Truncator

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Post, Comment

User = get_user_model()


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = {}
        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)


class UserRegisterSerializer(serializers.ModelSerializer):

    password = PasswordField()
    password2 = PasswordField()

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]
        if password != password2:
            raise serializers.ValidationError("password not match.")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "get_full_name"]


class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "timestamp"]

    def get_timestamp(self, obj):
        return obj.timestamp.strftime("%d-%m-%Y")


class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    truncated_content = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "slug",
            "content",
            "status",
            "comments",
            "truncated_content",
            "image",
            "detail_url",
            "comment_count",
            "timestamp",
        ]

    def get_comment_count(self, obj):
        return obj.posts.count()

    def get_detail_url(self, obj):
        request = self.context["request"]
        post_detail_url = request.build_absolute_uri(
            reverse("posts-detail", kwargs={"slug": obj.slug})
        )
        return post_detail_url

    def get_timestamp(self, obj: Post):

        return obj.timestamp.strftime("%c")

    def get_comments(self, obj):
        request = self.context["request"]
        query = int(request.query_params.get("comment_limits", 2))
        qs = obj.posts.order_by("-timestamp")[:query]
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
