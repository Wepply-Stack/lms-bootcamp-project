from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class that allows access only to admin users.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated and has admin role
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == 'admin'
        )
    
    def has_object_permission(self, request, view, obj):
        # For object-level permissions, also check admin role
        return self.has_permission(request, view)


class IsEmployee(permissions.BasePermission):
    """
    Permission class for employee users (optional, for employee-side routes)
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == 'employee'
        )

