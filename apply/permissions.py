from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

# 동아리 운영진에 대한 permission
class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_operator:
            return True
        raise PermissionDenied(detail="Request user is not crew administrator")