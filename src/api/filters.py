import django_filters

from posts.models import Post

class PostFilterSet(django_filters.FilterSet):

    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Post 
        fields = ['title', 'slug', 'tags', 'text']