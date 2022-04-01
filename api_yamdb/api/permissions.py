from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthenticatedUserModeratorAdminCreateObject(
    permissions.BasePermission
):
    """
    Отзыв могут создавать только Аутентифицированные пользователи:
    user, moderator, admin.
    """
    def has_object_permission(self, request, view, obj):
        if (request.method == 'OPTIONS' and 
            request.method in permissions.SAFE_METHODS):
            if obj.author is (request.user.is_authenticated or
                              request.user.is_moderator or
                              request.user.is_admin):
                return True
