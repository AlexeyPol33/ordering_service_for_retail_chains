from rest_framework import permissions
from .models import Order, OrderItem

class isAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class IsShopOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user

class isOrderOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj,Order):
            return request.user == obj.user
        elif isinstance(obj,OrderItem):
            return request.user == obj.order.user
        return False