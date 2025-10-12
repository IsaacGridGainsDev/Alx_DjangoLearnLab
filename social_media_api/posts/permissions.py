"""
Custom permissions for posts app - keeping things secure 🔒
"""

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission - authors can edit, everyone can view
    Like Wikipedia, but with more control 📚
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for author
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object owner permission - you can only mess with your own stuff 🔐
    """
    
    def has_object_permission(self, request, view, obj):
        # Everyone can read
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only owner can modify
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False