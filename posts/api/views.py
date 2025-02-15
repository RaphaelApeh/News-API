from rest_framework import generics, status
from rest_framework.response import Response

# from django_filters import rest_framework as filters

from .permissions import IsOwnerOrCanComment
from .pagination import PostsPageNumberPagination

from ..models import Post
# from ..filters import PostFilterSet
from ..serializers import (
    PostSerializer,
    CommentSerializer
    )


class PostListView(generics.ListCreateAPIView):
    """
    List of posts
    """
    queryset = Post.objects.select_related("user").order_by("-timestamp")
    serializer_class = PostSerializer
    pagination_class = PostsPageNumberPagination
    # filter_backends = [filters.DjangoFilterBackend]
    # filterset = PostFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get("user")
        if user:
            queryset = queryset.filter(user__username__icontains=user)
        return queryset
    

class PostRetrieveView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsOwnerOrCanComment]
    queryset = Post.objects.select_related("user").filter(active=True)
    lookup_field = "slug"
    serializer_class = PostSerializer

    def get_serializer_class(self):
        
        if self.request.method == "POST":
            return CommentSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """
        users can add comment to a post
        """
        serializer = self.get_serializer(data=self.request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": serializer.data["content"]}, status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(post=self.get_object(), user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)