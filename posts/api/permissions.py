from rest_framework import permissions


CUSTOM_METHOD = [
    "GET",
    "HEAD",
    "OPTIONS",
    "POST",
]  # users can add a comment with a POST request


class IsOwnerOrCanComment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if (request.user != obj.user) and request.method not in CUSTOM_METHOD:
            return False
        return True
