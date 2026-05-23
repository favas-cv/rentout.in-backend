from rest_framework.permissions import BasePermission


class IsActiveUsers(BasePermission):
    
    message ='Your account has been blocked.'
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_live
        )