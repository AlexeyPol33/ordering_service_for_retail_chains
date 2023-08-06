from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserTypeChoices(models.TextChoices):
    SHOP = 'Магазин'
    BUYER = 'Покупатель'    

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email addres'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=200,
        help_text=_('Required. 200 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts. '
        ),
    )
    type = models.CharField(verbose_name='Тип пользователя',
                             choices=UserTypeChoices.choices,
                             max_length=10,
                             default=UserTypeChoices.BUYER)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ('email',)

class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',unique=True)
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True,unique=True)
    filename = models.CharField(max_length=100, verbose_name='Название файла',blank=True,null=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)
    
    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    shops = models.ManyToManyField(Shop, through='ShopsCategories',blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список Категорий'
        ordering = ('-name',)

    def __str__(self) -> str:
        return self.name
    
class ShopsCategories(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    shops = models.ForeignKey(Shop,on_delete=models.CASCADE)

class Product(models.Model):
    category = models.ForeignKey(Category,verbose_name='Категория', null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name='Название')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Список Продуктов'
        ordering = ('-name',)
    
    def __str__(self) -> str:
        return self.name
    
class ProductInfo(models.Model):
    product = models.ForeignKey(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,verbose_name='Магазин', on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name='Название')
    quantity = models.FloatField(verbose_name='Количество',validators=[MinValueValidator(0)])
    price = models.FloatField(verbose_name='Цена',validators=[MinValueValidator(0)])
    price_rrc = models.FloatField(verbose_name='разрешенная розничная цена без НДС ')

class Parameter(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название',unique = True)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Список Параметров'
        ordering = ('-name',)
    
    def __str__(self) -> str:
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo,on_delete=models.CASCADE,verbose_name='Информация о продукте')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметер')
    value = models.TextField(verbose_name='Значение')


class Order(models.Model):
    class OrderStatusChoice(models.TextChoices):
        BASKET = 'Статус корзины'
        NEW = 'Новый'
        CONFIRMED = 'Подтвержден'
        ASSEMBLED = 'Собран'
        SENT = 'Отправлен'
        DELIVERED = 'Доставлен'
        CANCELED = 'Отменен'
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'

    user = models.ForeignKey(User, verbose_name='Пользователь',on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания')
    status = models.CharField(choices=OrderStatusChoice.choices,
                                default=OrderStatusChoice.NEW,
                                verbose_name='Статус')
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name='Заказ',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,verbose_name='Магазин',on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Количество')

class Contact(models.Model):
    type = models.CharField(max_length=100, verbose_name='Тип')
    user = models.ForeignKey(User,verbose_name='Пользователь',on_delete=models.CASCADE)
    value = models.CharField(max_length=100, verbose_name='значение')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Список контактов'