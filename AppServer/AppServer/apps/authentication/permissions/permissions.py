from rest_framework.permissions import BasePermission
class DumplogPermissions(BasePermission):
    def has_permissions(self, request, view):
        if request.method == 'GET' or request.user and request.user.is_staff():
            return True
        return False