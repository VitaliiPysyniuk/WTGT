from rest_framework.permissions import BasePermission

from .models import UserRoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role == UserRoleChoices.ADMINISTRATOR))


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR))
