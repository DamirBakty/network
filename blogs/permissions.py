from rest_framework import permissions

from blogs import models

class PostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT'] and obj.user == request.user:
            return True
        return False

    def has_permission(self, request, view):
        if request.method == 'GET' or models.Post.objects.get(pk=view.kwargs.get('pk')).user == request.user:
            return True
        return False
