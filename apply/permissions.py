from rest_framework import permissions

# 동아리 운영진에 대한 permission
class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_operator)