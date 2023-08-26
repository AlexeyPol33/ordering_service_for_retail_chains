from rest_framework import permissions
from .models import Order, OrderItem, Contact, User, Shop, Product, ProductInfo


class isAccountOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        elif isinstance(obj, Contact):
            return request.user == obj.user


class IsShopOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_anonymous:
            return False
        if request.user.position != User.UserPositionChoices.SHOP_OWNER:
            return False
        if isinstance(obj, Shop):
            return request.user.company == obj
        elif isinstance(obj, Product):
            product_info = ProductInfo.objects.get(id=obj.id)
            return request.user.company == product_info.shop
        elif isinstance(obj, ProductInfo):
            return request.user.company == obj.shop
        else:
            request.user.company == obj.shop


class isOrderOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Order):
            return request.user == obj.user
        elif isinstance(obj, OrderItem):
            return request.user == obj.order.user
        return False
