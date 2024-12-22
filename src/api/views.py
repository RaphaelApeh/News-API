from django.shortcuts import get_object_or_404

from rest_framework import permissions, authentication, parsers, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes

from posts.models import Post
from .serializers import PostSerializer
from .services import PostPagination
from .filters import PostFilterSet


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def list_posts_view(request):
    paginator = PostPagination()
    filters = PostFilterSet(request.GET, queryset=Post.objects.select_related('user').all())
    qs = filters.qs
    post_response = paginator.paginate_queryset(qs, request)
    serializer = PostSerializer(post_response, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([authentication.TokenAuthentication])
def detail_post_view(request, slug: str):
    post = get_object_or_404(Post, slug=slug)
    serializer = PostSerializer(post, many=False)    
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([parsers.MultiPartParser, parsers.FormParser])
def create_post_view(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    

class CreatePostView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    