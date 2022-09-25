from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Ограничение доступа только для администратора"""
    message = 'Доступ только для администрации!'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminModerAuthorOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только администратору, модератору и автору.
    Запрещает отправлять POST-запросы не аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Всем пользователям разрешается делать безопасные запросы, небезопасные
    запросы - только администратору
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin
