from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from posts.models import Post
from .serializers import PostSerializer
from .filters import PostFilterSet


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def list_posts_view(request):
    print(f'{request.headers.values()=}')
    filters = PostFilterSet(request.GET, queryset=Post.objects.select_related('user').all())
    qs = filters.qs
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)