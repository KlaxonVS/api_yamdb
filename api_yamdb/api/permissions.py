from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Ограничение доступа только для администратора"""
    message = 'Доступ только для администрации!'

    def has_permission(self, request, view):
        return request.user.is_admin
