from rest_framework.permissions import BasePermission
class DumplogPermissions(BasePermission):
    def has_permissions(self, request, view):
        if request.data.get('username', None) is not None and not request.user.is_staff():
            return True
        if request.data.get('username', None) and request.user.is_staff():
            return True
        return False