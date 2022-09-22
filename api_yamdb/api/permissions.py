from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Ограничение доступа только для администратора"""
    message = 'Доступ только для администрации!'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только админинстратору, модератору и автору.
    Запрещает отправлять POST-запросы не аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)

        return (request.user.is_moderator or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
