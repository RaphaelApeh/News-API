from django.db import models
from django.template import loader
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.core.exceptions import FieldError
from rest_framework.filters import BaseFilterBackend


class PostFilterBackend(BaseFilterBackend):

    template_name = "posts/form.html"

    def _query_params(self, request, /):
        return request.query_params.copy()


    def filter_queryset(self, request, queryset, view):
        if not hasattr(view, "search_fields"):
            return queryset.none() # []
        fields = getattr(view, "search_fields")
        query_params = getattr(view, "query_params", "search")
        _query = self._query_params(request).get(query_params)
        if _query is not None:
            query = models.Q()
            for field in fields:
                query |= models.Q(**{"%s__icontains" % field: _query})
            try:
                return queryset.filter(query)
            except FieldError:
                return queryset.none()
        return queryset.all()
    
    def to_html(self, request, queryset, view):

        if not getattr(view, "search_fields", None):
            return ""
        template = loader.get_template(self.template_name)
        query_params = getattr(view, "query_params", "search")
        context = {
            "query_params": query_params
        }
        return template.render(context, request)
                