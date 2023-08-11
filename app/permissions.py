from rest_framework import permissions

class isAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsShopOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator