from rest_framework import permissions
from rest_framework.views import PermissionDenied


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if not request.user or request.user.is_anonymous:
            raise PermissionDenied()
        return super().has_permission(request, view)
