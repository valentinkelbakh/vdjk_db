from rest_framework.permissions import IsAuthenticated, BasePermission

class CustomUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_perm('home.change_model')
        elif request.method == 'DELETE':
            return request.user.has_perm('home.delete_model')
        return False
