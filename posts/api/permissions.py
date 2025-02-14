from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.user != obj.user and request.method not in permissions.SAFE_METHODS:
            return False
        return True