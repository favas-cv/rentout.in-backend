from rest_framework.permissions import BasePermission


class IsOwnerUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            # getattr(request.user,'is_owner', False)
            request.user.is_owner and
            request.user.is_verified and 
            request.user.kyc_status == 'VERIFIED' and
            request.user.is_live
            
        ) 
        

class IsOwnerDashboardUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and  
            request.user.is_owner
        )