from rest_framework import pagination, status
from rest_framework.response import Response


class PostsPageNumberPagination(pagination.PageNumberPagination):

    page_size = 5
    page_query_param = "posts"

    def get_paginated_response(self, data):

        return Response(
            {
                "status": "ok",
                "total_pages": self.page.paginator.num_pages,
                "current_count": len(data),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "posts": data,
            },
            status.HTTP_200_OK,
        )
