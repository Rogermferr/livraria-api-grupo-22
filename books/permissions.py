from rest_framework import permissions
from users.models import User
from rest_framework.views import View, Request


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
