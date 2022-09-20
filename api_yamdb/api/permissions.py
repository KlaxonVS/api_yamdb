from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Ограничение доступа только для администратора или суперюзера"""
    message = 'Доступ только для администрации!'

    def has_permission(self, request, view):
        return request.user.ADMIN
