from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from app.models import Shop,ShopsCategories,Category,Product,\
ProductInfo,Parameter,ProductsParameters,Order,\
OrderItem,Contact, User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from .yaml_data_dump import db_dump
from django.core.mail import send_mail
from django.http import HttpRequest
from os import getenv
from rest_framework.parsers import MultiPartParser, FileUploadParser
import yaml
from django.http import HttpResponseNotAllowed,HttpResponseNotFound,HttpResponseBadRequest
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework.authentication import BasicAuthentication
from app.permissions import isAccountOwnerPermission, IsShopOwnerPermission,\
isOrderOwnerPermission
from app.serializers import ShopSerializer,ProductSerializer,\
ProductInfoSerializer,OrderSerializer,OrderItemSerializer,\
ContactSerializer, UserSerializer

def test_send_email():
    subject = 'Тест почтовой службы'
    message = 'Проверка работы почтовой службы, тестовое сообщение'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient@example.com']
    send_mail(subject, message, from_email, recipient_list,fail_silently=False)

def home (request):
    return HttpResponse('Home page')

# аутентификация и управление профилем

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

    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in ['update', 'partial_update','destroy','retrieve',]:
            permission_classes = [isAccountOwnerPermission|IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]

#Управление магазином и продуктами

class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update','destroy']:
            permission_classes = [IsShopOwnerPermission|IsAdminUser]
        elif self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]

class MakeShopOwner(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self,request):
        pass

class PartnerUpdate(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        try:
            user = request.user
            if user.is_anonymous:
                return HttpResponse('Authorization error',status=401)
        except:
            return HttpResponse('Authorization error',status=401)
        
        try:
            if user.position != User.UserPositionChoices.SHOP_OWNER:
                return HttpResponse('user is not shop owner',status=403)
            shop = user.company
        except:
            return HttpResponse('Forbidden',status=403)

        uploaded_file = ''
        try:
            uploaded_file = request.FILES['file']
        except:
            return HttpResponse('file not provided',status=400)
        try:
            file_content = uploaded_file.read().decode('utf-8')
            yaml_data = yaml.safe_load(file_content)
        except yaml.YAMLError as e:
            return HttpResponse(f'Error reading yaml file: {e}',status=400)
        
        try:
            db_dump(yaml_data,shop=shop)
        except:
            return HttpResponse('Error writing yaml file.',status=400)
        
        return HttpResponse('Created.',status=201)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsShopOwnerPermission]
        elif self.action in ['update', 'partial_update','destroy']:
            permission_classes = [IsShopOwnerPermission|IsAdminUser]
        elif self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]

class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsShopOwnerPermission|IsAdminUser]
        elif self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]

# Управление корзиной
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update','destroy','retrieve','list']:
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
        elif self.action in ['update', 'partial_update','destroy','retrieve','list']:
            permission_classes = [IsAdminUser|isOrderOwnerPermission]
        else:
            return []
        return [permission() for permission in permission_classes]

class OrderConfirmation(APIView):
    queryset = Order.objects.all()
    def post(self,request):
        try:
            user = request.user
            if user.is_anonymous:
                return HttpResponseBadRequest('Authorization error')
                
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