from rest_framework.serializers import ModelSerializer
from rest_framework import validators
from app.models import Shop,ShopsCategories,Category,Product,\
ProductInfo,Parameter,ProductParameter,Order,\
OrderItem,Contact, User



class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id','name','url','filename']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','shops']

class ShopsCategoriesSerializer:
    class Meta:
        model = ShopsCategories
        fields = ['id','categories','shops']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','category',' name']


class ProductInfoSerializer(ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['id','product','shop','name','quantity','price','price_rrc']

class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id','name']

class ProductParameterSerializer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['id','product_info','parameter','value']

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','dt','status']

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order','product','shop','quantity']

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','type','user','value']

class UserSerializer(ModelSerializer):
    class Meta:
        model =  User
        fields = ['id','username','password','email','company','position']