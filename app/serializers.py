from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .tasks import send_registration_confirmation_email
from app.models import Shop, Product, \
    ProductInfo, ProductsParameters, Order, \
    OrderItem, Contact, User


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'categories']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        categories_data = self.context['request'].data.get('categories', None)

        if categories_data:

            instance.add_categories(categories_data)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):

    class CategoriesCustomField(serializers.Field):
        def to_representation(self, categories):
            return ', '.join(category.name for category in categories.all())

        def to_internal_value(self, data):
            return data

    categories = CategoriesCustomField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'categories']

    def create(self, validated_data):
        product = Product()
        try:
            product.id = validated_data['id']
        except KeyError:
            pass
        product.name = validated_data['name']
        product.save()
        if validated_data.get('categories', None):
            print(product)
            product.add_categories(validated_data['categories'])
        product.save()
        ProductInfo.objects.create(
            product=product,
            shop=self.context['request'].user.company
        )

        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if validated_data.get('categories', None):
            instance.add_categories(validated_data['categories'])
        instance.save()
        return instance


class ProductInfoSerializer(serializers.ModelSerializer):

    class ParametersCustomField(serializers.Field):
        def to_representation(self, parameters):
            view = self.context['view']
            product_info = view.get_object()

            parameters_values = []
            for p in parameters.all():
                value = ProductsParameters.objects.get(
                    product_info=product_info,
                    parameter=p
                    ).value
                parameters_values.append(f'{p.name} {value}')
            return ', '.join(parameter for parameter in parameters_values)

        def to_internal_value(self, data):
            return data

    parameters = ParametersCustomField(required=False)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'name',
                        'quantity', 'parameters',
                        'price', 'price_rrc']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.price_rrc = validated_data.get(
            'price_rrc',
            instance.price_rrc
            )

        if validated_data.get('parameters', None):
            instance.add_parameters(validated_data['parameters'])
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):

    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'dt', 'status', 'total_cost']

    def get_total_cost(self, obj):
        orders_items = OrderItem.objects.filter(order=obj).all()
        total_cost = 0
        for item in orders_items:
            total_cost += ProductInfo.objects.get(
                product=item.product).price * item.quantity

        return total_cost

    def delete(self, instance):
        if instance.status == Order.OrderStatusChoice.DELIVERED:
            raise serializers.ValidationError(
                'You cannot delete an order that has already been delivered'
                )
        instance.delete()
        return {'message': 'Order successfully canceled'}


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity']

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        required=False
        )

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
                shop=shop
                )
        except Order.DoesNotExist:
            order = Order.objects.create(
                user=user,
                status=Order.OrderStatusChoice.NEW,
                shop=shop
                )

        validated_data['product'] = product
        validated_data['order'] = order

        try:
            orderitem = OrderItem.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(f'Error: {e}')
        return orderitem

    def delete(self, instance):

        if instance.order.status == Order.OrderStatusChoice.DELIVERED:
            raise serializers.ValidationError(
                'You cannot delete an item that has already been delivered'
                )
        instance.delete()
        return {'message': 'Item successfully canceled'}


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'phone', 'country',
                  'region', 'locality', 'street',
                  'house', 'description']

    def update(self, instance, validated_data):

        try:
            instance.phone = validated_data.get('phone', instance.phone)
        except Exception:
            pass
        instance.country = validated_data.get(
            'country', instance.country
            )
        instance.region = validated_data.get(
            'region', instance.region
            )
        instance.locality = validated_data.get(
            'locality', instance.locality
            )
        instance.street = validated_data.get(
            'street', instance.street)
        instance.house = validated_data.get(
            'house', instance.house
            )
        instance.description = validated_data.get(
            'description', instance.description
            )

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

        model = User
        fields = ['id', 'username', 'password', 'email', 'company', 'position']
        extra_kwargs = {
            'password': {'write_only': True},
            'company': {'read_only': True},
            'position': {'read_only': True},
        }

    def create(self, validated_data):

        user = User.objects.create(

            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()
        send_registration_confirmation_email.delay(user.email, user.id)

        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
