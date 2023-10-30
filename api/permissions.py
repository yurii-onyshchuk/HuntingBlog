from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission class for read-only access to views and admin access.

    This permission class is used to restrict write (POST, PUT, DELETE) access to views to users who are
    staff members (administrators), while allowing read (GET) access to all users, including anonymous users.
    """

    def has_permission(self, request, view):
        """Return `True` if permission is granted, `False` otherwise."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class SubscribePermission(permissions.BasePermission):
    """Custom permission class for subscription management.

    This permission class defines the access control rules for managing email subscriptions.
    It allows certain actions based on the user's authentication status and the action being performed.
    """

    def has_permission(self, request, view):
        """Return `True` if permission is granted, `False` otherwise."""
        if view.action == 'create':
            return True
        if view.action in ['retrieve', 'destroy'] and request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Return `True` if permission is granted, `False` otherwise."""
        if view.action in ['retrieve', 'destroy'] and request.user and request.user.email == obj.email:
            return True
        return False
