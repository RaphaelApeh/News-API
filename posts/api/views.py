from rest_framework import generics

from ..models import Post
from ..serializers import PostSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer