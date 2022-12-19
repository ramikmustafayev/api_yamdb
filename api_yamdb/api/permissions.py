from rest_framework import permissions



class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return  request.user.role=='admin' or request.user.is_superuser

class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        return request.user==obj.author or request.user.role=='moderator' or  request.user.role=='admin' or request.user.is_superuser