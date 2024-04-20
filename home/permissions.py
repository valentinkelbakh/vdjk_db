from rest_framework.permissions import BasePermission


class CustomUserPermission(BasePermission):
    def __check_user(self, request) -> bool:
        if request.user.is_superuser:
            return True

        if request.method == "POST":
            return request.user.is_active and request.user.has_perm("home.add_model")

        if request.method in ["PUT", "PATCH"]:
            return request.user.is_active and request.user.has_perm("home.change_model")

        if request.method == "DELETE":
            return request.user.is_active and request.user.has_perm("home.delete_model")

    def has_permission(self, request, view):
        return self.__check_user(request)

    def has_object_permission(self, request, view, obj):
        return self.__check_user(request)
