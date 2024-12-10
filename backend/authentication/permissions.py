from rest_framework.permissions import BasePermission
class HasRolePermission(BasePermission):
    def has_permission(self, request,view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        required_roles = view.required_roles
        if not required_roles:
            return True
        return user.role.name == required_roles
