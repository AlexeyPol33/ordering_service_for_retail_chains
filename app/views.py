from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from app.models import Shop, Product, ProductInfo, \
    Order, OrderItem, Contact, User
from .tasks import db_dump
from django.core.mail import send_mail
from rest_framework.parsers import FileUploadParser
import yaml
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from celery.result import AsyncResult
from social_django.models import UserSocialAuth
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.tokens import RefreshToken
from app.permissions import isAccountOwnerPermission, \
    IsShopOwnerPermission, isOrderOwnerPermission
from app.serializers import ShopSerializer, ProductSerializer, \
    ProductInfoSerializer, OrderSerializer, OrderItemSerializer, \
    ContactSerializer, UserSerializer


def home(request):
    return HttpResponse('Home page')

def social_auth_callback(request):
    user = request.user  
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return HttpResponse("access_token: {}".format(access_token))


# аутентификация и управление профилем
@extend_schema(tags=['User'])
@extend_schema_view(
    list=extend_schema(summary='Получить список пользователей'),
    retrieve=extend_schema(summary='Получить пользователя'),
    partial_update=extend_schema(summary='Обновить пользователя'),
    create=extend_schema(summary='Зарегистрировать нового пользователь'),)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in [
            'update', 'partial_update',
                'destroy', 'retrieve',]:
            permission_classes = [isAccountOwnerPermission | IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]
    
class ConfirmRegistration(APIView):
    
    def get(self, request, task_id, *args, **kwargs):
        try:
            task = AsyncResult(task_id)
        except Exception as e:
            return HttpResponse(f'Err: {e}',status=400)
        if task.ready():
            user = User.objects.get(id=task.get())
            user.is_active = True
            user.save()
            RefreshToken.for_user(user)
            return HttpResponse('Регистрация подтверждена',status=200)
        else:
            return HttpResponse('',status=404)
            

        

@extend_schema(tags=['Contact'])
@extend_schema_view(
    retrieve=extend_schema(summary='Получить контактную информацию пользователя'),
    partial_update= extend_schema(summary='Обновить контактную информацию пользователя'),
)
class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in [
            'update', 'partial_update',
                'destroy', 'retrieve',]:
            permission_classes = [isAccountOwnerPermission | IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]


# Управление магазином и продуктами
@extend_schema(tags=['Shop'])
@extend_schema_view(
    list= extend_schema(summary='Получить список магазинов'),
    retrieve=extend_schema(summary='Получить магазин'),
    partial_update= extend_schema(summary='Обновить магазин'),
    create= extend_schema(summary='Создать магазин'),)
class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsShopOwnerPermission | IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]

@extend_schema(tags=['Shop'])
@extend_schema_view(
    create= extend_schema(summary='Зделать пользователя владельцем магазина'),)
class MakeShopOwner(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request):
        pass

@extend_schema(tags=['Shop'])
@extend_schema_view(
    retrieve=extend_schema(summary='Получить статус загрузки файла'),
    create= extend_schema(summary='Загрузить yaml файл'),)
class PartnerUpdate(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        try:
            user = request.user
            if user.is_anonymous:
                return HttpResponse('Authorization error', status=401)
        except Exception:
            return HttpResponse('Authorization error', status=401)

        try:
            if user.position != User.UserPositionChoices.SHOP_OWNER:
                return HttpResponse('user is not shop owner', status=403)
            shop = user.company
        except Exception as e:
            return HttpResponse(f'err: {e}', status=403)

        uploaded_file = ''
        try:
            uploaded_file = request.FILES['file']
        except KeyError:
            return HttpResponse('file not provided', status=400)
        try:
            file_content = uploaded_file.read().decode('utf-8')
            yaml_data = yaml.safe_load(file_content)
        except yaml.YAMLError as e:
            return HttpResponse(f'Error reading yaml file: {e}', status=400)

        try:
            delay = db_dump.delay(yaml_data, shop=shop.id)
        except Exception as e:
            return HttpResponse(f'Error writing yaml file: {e}', status=400)

        return HttpResponse(f'Created. Tasks_id:{delay.id}', status=201)
    
    def get(self, request, task_id,*args, **kwargs):
        try:
            task = AsyncResult(task_id)
        except Exception as e:
            return HttpResponse(f'Err: {e}',status=400)
        status = task.status
        return HttpResponse(f'task status: {status}', status=200)


@extend_schema(tags=['Product'])
@extend_schema_view(
    list=extend_schema(summary='Получить список продуктов'),
    retrieve=extend_schema(summary='Получить продукт'),
    partial_update=extend_schema(summary='Обновить продукт'),
    create=extend_schema(summary='Создать продукт'),)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsShopOwnerPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsShopOwnerPermission | IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]


@extend_schema(tags=['Product'])
@extend_schema_view(
    list= extend_schema(summary='Получить развернутый список продуктов'),
    retrieve=extend_schema(summary='Получить информацию о продукте'),
    partial_update= extend_schema(summary='Обновить информацию о продукте'),
    )
class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsShopOwnerPermission | IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            return []
        return [permission() for permission in permission_classes]


# Управление корзиной
@extend_schema(tags=['Order'])
@extend_schema_view(
    list= extend_schema(summary='Получить список заказов'),
    retrieve=extend_schema(summary='Получить заказ'),
    partial_update= extend_schema(summary='Обновить заказ'),
    create= extend_schema(summary='Создать заказ'),)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in [
            'update', 'partial_update',
                'destroy', 'retrieve', 'list']:
            permission_classes = [IsAdminUser | isOrderOwnerPermission]
        else:
            return []
        return [permission() for permission in permission_classes]

@extend_schema(tags=['Order'])
@extend_schema_view(
    retrieve=extend_schema(summary='Получить содержимое заказа'),
    partial_update= extend_schema(summary='Изменить содержимое заказа'),
    create= extend_schema(summary='Добавить товар в заказ'),)
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(order__user=user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in [
                'destroy', 'retrieve', 'list']:
            permission_classes = [IsAdminUser | isOrderOwnerPermission]
        else:
            return []
        return [permission() for permission in permission_classes]

@extend_schema(tags=['Order'])
@extend_schema_view(
    create= extend_schema(summary='Подтвердить заказ'),)
class OrderConfirmation(APIView):
    queryset = Order.objects.all()

    def post(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                return HttpResponseBadRequest('Authorization error')

        except Exception as e:
            return HttpResponseBadRequest(f'Authorization error: {e}')
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
                return HttpResponseBadRequest(
                    f'To confirm the order,\
                    you need to fill in the following\
                    contact fields:{contact_bad_field}')
        except Exception as e:
            return HttpResponseBadRequest(f'contact error:{e}')
        try:
            orders = Order.objects.filter(
                user=user,
                status=Order.OrderStatusChoice.NEW
                )
        except Exception as e:
            return HttpResponseNotFound(f'Orders not found; err: {e}')
        for order in orders:
            order.status = Order.OrderStatusChoice.CONFIRMED
            order.save()
        return HttpResponse('detail: All orders have\
                         changed their status to confirmed', status=200)
