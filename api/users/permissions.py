from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', '') == 'moderator'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if view.kwargs['username'] == 'me' and request.user.role:
                return True
        except Exception:
            pass
        try:
            return request.user.role == 'admin'
        except Exception:
            return False


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PATCH']:
            return obj == request.user
        return False
