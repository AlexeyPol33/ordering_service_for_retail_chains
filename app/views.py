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
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from app.permissions import isAccountOwnerPermission, IsShopOwnerPermission
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
        if self.action == 'create':
            permission_classes = [AllowAny]
        if self.action in ['update', 'partial_update','destroy','retrieve','list']:
            permission_classes = [isAccountOwnerPermission|IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]

        
class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


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

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update','destroy','retrieve','list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer