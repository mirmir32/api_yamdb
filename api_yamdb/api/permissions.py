from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


# class IsAuthenticatedUserModeratorAdminCreateObject(
#     BasePermission
# ):
#     """
#     Отзыв могут создавать только Аутентифицированные пользователи:
#     user, moderator, admin.
#     """
#     def has_object_permission(self, request, view, obj):
#         if (request.method == 'OPTIONS' and
#             request.method in SAFE_METHODS):
#             if obj.author is (request.user.is_authenticated or
#                               request.user.is_moderator or
#                               request.user.is_admin):
#                 return True


class IsObjectOwnerModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
