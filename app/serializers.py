from rest_framework import serializers
from rest_framework import validators
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.models import Shop,ShopsCategories,Category,Product,\
ProductInfo,Parameter,ProductParameter,Order,\
OrderItem,Contact, User


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id','name','url','filename']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','shops']

class ShopsCategoriesSerializer:
    class Meta:
        model = ShopsCategories
        fields = ['id','categories','shops']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','category','name']

class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ['id','product','shop','name','quantity','price','price_rrc']

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id','name']

class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['id','product_info','parameter','value']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','dt','status']

class OrderItemSerializer(serializers.ModelSerializer): #TODO добавить валидацию количества товара
    class Meta:
        model = OrderItem
        fields = ['id','order','product','quantity']

    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)

    def create(self, validated_data):

        user = self.context['request'].user
        try:
            product = validated_data['product']
            shop = ProductInfo.objects.get(product=product).shop
        except Product.DoesNotExist:
            raise serializers.ValidationError('Продукт не найден.')

        try:
            order = Order.objects.get(
                user=user,
                status=Order.OrderStatusChoice.NEW,
                shop = shop
                )
        except Order.DoesNotExist:
            order = Order.objects.create(
                user=user,
                status=Order.OrderStatusChoice.NEW,
                shop = shop
                )
            order.save()
        
        validated_data['product'] = product
        validated_data['order'] = order
        
        orderitem = OrderItem.objects.create(**validated_data)
        orderitem.save()
        return orderitem

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id','user','phone','country','region','locality','street','house','description']
    def update(self, instance, validated_data):

        try:
            instance.phone = validated_data.get('phone', instance.phone)
        except:
            pass
        instance.country = validated_data.get('country', instance.country)
        instance.region = validated_data.get('region', instance.region)
        instance.locality = validated_data.get('locality', instance.locality)
        instance.street = validated_data.get('street', instance.street)
        instance.house = validated_data.get('house', instance.house)
        instance.description = validated_data.get('description', instance.description)
        

        instance.save()
        return instance

class ObtainTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['id','username','password','email','company','position']

    def create(self, validated_data):
        user = User.objects.create(

            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        send_mail(
            subject = 'Подтвердите регистрацию',
            message = 'Для подтверждения регистрации перейдите по ссылке:',
            from_email = 'your_email@example.com', 
            recipient_list = [user.email],
            fail_silently=False
            )
        user.is_active = True
        user.save()
        contact = Contact.objects.create(user=user)
        contact.save()
        return user
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)