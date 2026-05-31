from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    # Only the author can edit or delete this object.

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        

        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False