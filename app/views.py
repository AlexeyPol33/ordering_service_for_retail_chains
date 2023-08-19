from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from app.models import Shop,ShopsCategories,Category,Product,\
ProductInfo,Parameter,ProductParameter,Order,\
OrderItem,Contact, User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from os import getenv
from django.http import HttpResponseNotAllowed,HttpResponseNotFound,HttpResponseBadRequest
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from app.permissions import isAccountOwnerPermission, IsShopOwnerPermission,\
isOrderOwnerPermission
from app.serializers import ShopSerializer, ShopsCategoriesSerializer,\
CategorySerializer, ProductSerializer, ProductInfoSerializer,\
ParameterSerializer, ProductParameterSerializer, OrderSerializer,\
OrderItemSerializer, ContactSerializer, UserSerializer, ObtainTokenSerializer

def test_send_email():
    subject = 'Тест почтовой службы'
    message = 'Проверка работы почтовой службы, тестовое сообщение'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient@example.com']
    send_mail(subject, message, from_email, recipient_list,fail_silently=False)

def home (request):
    return HttpResponse('Home page')

# аутентификация и управление профелем
class ObtainTokenView(TokenObtainPairView):
    serializer_class = ObtainTokenSerializer

class RefreshTokenView(APIView):
    def post(self,request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)

        try:
            access_token = str(refresh.access_token)
        except:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'access': access_token})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update','destroy','retrieve',]:
            permission_classes = [isAccountOwnerPermission|IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
        
class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    def get_permissions(self):
        return super().get_permissions()


class ShopsCategoriesViewSet(ModelViewSet):
    queryset = ShopsCategories.objects.all()
    serializer_class = ShopsCategoriesSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

class ParameterViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer

class ProductParameterViewSet(ModelViewSet):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update','destroy','retrieve','list']:
            permission_classes = [IsAdminUser|isOrderOwnerPermission]
        else:
            return []
        return [permission() for permission in permission_classes]

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update','destroy','retrieve','list']:
            permission_classes = [IsAdminUser|isOrderOwnerPermission]
        else:
            return []
        return [permission() for permission in permission_classes]

class OrderConfirmation(APIView):
    def post(self,request):
        try:
            user = request.user
        except:
            return HttpResponseBadRequest('Authorization error')
        try:
            contact = Contact.objects.get(user=user)
            contact_bad_field = []
            if not contact.phone:
                contact_bad_field.append('phone')
            if not contact.country:
                contact_bad_field.append('country')
            if not contact.region:
                contact_bad_field.append('region')
            if not contact.locality:
                contact_bad_field.append('locality')
            if not contact.street:
                contact_bad_field.append('street')
            if not contact.house:
                contact_bad_field.append('house')
            if contact_bad_field:
                return HttpResponseBadRequest(f'To confirm the order,\
                                               you need to fill in the following\
                                               contact fields:{contact_bad_field}')
        except:
            return HttpResponseBadRequest('contact error')
        try:
            orders = Order.objects.filter(
                user=user,
                status=Order.OrderStatusChoice.NEW
                )
        except:
            return HttpResponseNotFound('Orders not found')
        for order in orders:
            order.status = Order.OrderStatusChoice.CONFIRMED
            order.save()
        return Response('All orders have\
                         changed their status to confirmed')

