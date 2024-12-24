from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import permissions, authentication, parsers, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes

from posts.models import Post
from .serializers import PostSerializer
from .services import PostPagination
from .filters import PostFilterSet

User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def list_posts_view(request):
    paginator = PostPagination()
    filters = PostFilterSet(request.GET, queryset=Post.objects.select_related('user').all())
    qs = filters.qs
    post_response = paginator.paginate_queryset(qs, request)
    serializer = PostSerializer(post_response, many=True, context={'exclude': ['image']})
    serializer.context['request'] = request
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
def detail_post_view(request, slug: str):
    post = get_object_or_404(Post, slug=slug)
    print(request.META.get('HTTP_AUTHORIZATION'))
    serializer = PostSerializer(post, many=False, context={'exclude':['detail_url', 'image']})    
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([parsers.MultiPartParser, parsers.FormParser])
def create_post_view(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_post_like_view(request, slug):

    user = request.user
    
    try:
        
        post = Post.objects.get(slug__iexact=slug)
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'Success':'user has unliked a post.'})
        
        post.likes.add(user)
        return Response({'Success':'user has liked a post.'})
    except Post.DoesNotExist:

        return Response({'Error':'post_id does not exists.'}, status=status.HTTP_404_NOT_FOUND)

class CreatePostView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer