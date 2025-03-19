from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# from django_filters import rest_framework as filters

from .permissions import IsOwnerOrCanComment
from .pagination import PostsPageNumberPagination

from ..models import Post
# from ..filters import PostFilterSet
from ..serializers import (
    PostSerializer,
    CommentSerializer,
    UserRegisterSerializer
    )


User = get_user_model()


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

    permission_classes = [IsOwnerOrCanComment, IsAuthenticated]
    queryset = Post.objects.select_related("user").filter(active=True)
    lookup_field = "slug"
    serializer_class = PostSerializer

    def get_serializer_class(self):
        
        if self.request.method == "POST":
            return CommentSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if isinstance(response, Response):
            response.data["can_edit_or_update"] = request.user == self.get_object().user
        return response

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
    

class UserPostsListView(generics.ListAPIView):

    queryset = Post.objects.prefetch_related("posts")
    serializer_class = PostSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)



class UserRegisterView(generics.ListCreateAPIView):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = []
    authentication_classes = []


class TokenObtainView(TokenObtainPairView):

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        username = request.data["username"]
        password = request.data["password"]
        user = self.get_user(username=username, password=password)
        data = serializer.validated_data
        if user is not None:
            data = {
                "user_id": user.pk,
                "username": user.username,
                "refresh": serializer.validated_data["refresh"],
                "access": serializer.validated_data["access"]
            }
        return Response(data, status=status.HTTP_200_OK)
    
    @classmethod
    def get_user(cls, username, password):
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            return user if user.check_password(password) else None