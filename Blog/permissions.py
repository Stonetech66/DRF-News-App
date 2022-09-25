from rest_framework import permissions
from django.contrib.auth.hashers import check_password



class IsCommentOwner(permissions.BasePermission):
 def has_object_permission(self, request, view, obj ):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.name

class IsUserProfileOwner(permissions.BasePermission):
     def has_object_permission(self, request, view, obj ):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id == obj.user.id 
        

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True





