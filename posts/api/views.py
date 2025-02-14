from rest_framework import generics

from ..models import Post
from ..serializers import PostSerializer


class PostListView(generics.ListCreateAPIView):
    """
    List of posts
    """
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get("user")
        if user:
            queryset = queryset.filter(user__username__icontains=user)
        return queryset