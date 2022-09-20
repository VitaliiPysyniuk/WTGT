from rest_framework.permissions import BasePermission

from .models import UserRoleChoices


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == UserRoleChoices.ADMINISTRATOR)


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR)


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == UserRoleChoices.EMPLOYEE)


# class IsRestaurantAdminOrSystemAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and (request.user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR or
#                                  request.user.role == UserRoleChoices.ADMINISTRATOR)


class IsAdminOfCertainRestaurantOrSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == UserRoleChoices.ADMINISTRATOR
                                 or (request.user.role == UserRoleChoices.RESTAURANT_ADMINISTRATOR and
                                     view.kwargs.get('restaurant_id') == request.user.id))
