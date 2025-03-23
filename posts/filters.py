from django.db import models
from django.core.exceptions import FieldError
from rest_framework.filters import BaseFilterBackend


class PostFilterBackend(BaseFilterBackend):

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
                