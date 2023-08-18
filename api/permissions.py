from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit/delete, but allow all users to view.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class SubscribePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if view.action in ['retrieve', 'destroy'] and request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'destroy'] and request.user and request.user.email == obj.email:
            return True
        return False
