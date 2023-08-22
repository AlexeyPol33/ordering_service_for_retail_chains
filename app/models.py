from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _  

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список Категорий'
        ordering = ('-name',)

    def __str__(self) -> str:
        return self.name

class Shop(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название',unique=True)
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True,unique=True)
    categories = models.ManyToManyField(Category, through='ShopsCategories',blank=True,verbose_name='Категории')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def add_categories(self,category:str|list):
        if isinstance(category, str):
            category,c = Category.objects.get_or_create(name=category)
            self.categories.add(category)
        elif isinstance(category, list):
            for cat in category:
                category,c = Category.objects.get_or_create(name=category)
                self.categories.add(category)
        else:
            raise

    def __str__(self) -> str:
        return self.name

class ShopsCategories(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    shops = models.ForeignKey(Shop,on_delete=models.CASCADE)


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
    class UserPositionChoices(models.TextChoices):
        SHOP_OWNER = 'Владелец магазина'
        BUYER = 'Покупатель'

    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email addres'), unique=True)
    company = models.ForeignKey(
        Shop,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Компания'
        )
    position = models.CharField(
        choices=UserPositionChoices.choices,
        default=UserPositionChoices.BUYER,
        verbose_name='Позиция'
        )
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
    
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Список пользователей'
        ordering = ('email',)

class Contact(models.Model):

    user = models.OneToOneField(User,verbose_name='Пользователь',on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True,blank=True)
    country = models.CharField(max_length=20,verbose_name='страна',null=True, blank=True)
    region = models.CharField(max_length=20,verbose_name='регион',null=True, blank=True)
    locality = models.CharField(max_length=50,verbose_name='населенный пункт',null=True, blank=True)
    street = models.CharField(max_length=50,verbose_name='улица',null=True, blank=True)
    house = models.CharField(max_length=50,verbose_name='дом',null=True, blank=True)
    description = models.TextField(null=True, blank=True,verbose_name='Описание')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Список контактов'

class Parameter(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название',unique = True)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Список Параметров'
        ordering = ('-name',)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):

    categories = models.ManyToManyField(Category,through='ProductsCategories',blank=True,null=True)
    name = models.CharField(max_length=100,verbose_name='Название')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Список Продуктов'
        ordering = ('-name',)
    
    def add_categories(self,category:str|list):
        if isinstance(category, str):
            category,c = Category.objects.get_or_create(name=category)
            self.categories.add(category)
        elif isinstance(category, list):
            for cat in category:
                category,c = Category.objects.get_or_create(name=category)
                self.categories.add(category)
        else:
            raise

    def __str__(self) -> str:
        return self.name

class ProductInfo(models.Model):
    product = models.OneToOneField(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,verbose_name='Магазин', on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name='Название')
    parameters = models.ManyToManyField(Parameter,through='ProductsParameters',verbose_name='Параметры',blank=True,null=True)
    quantity = models.FloatField(verbose_name='Количество',validators=[MinValueValidator(0)],default=0)
    price = models.FloatField(verbose_name='Цена',validators=[MinValueValidator(0)],default=0)
    price_rrc = models.FloatField(verbose_name='разрешенная розничная цена без НДС ',default=0)

    def add_parameter(self, parameter, value=None):
        self.parameters.add(parameter)
        if value:
            products_parameter = ProductsParameters.objects.get(parameter=parameter,product_info=self)
            products_parameter.value = value
            products_parameter.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.product.pk
            self.name = self.product.name
        super(ProductInfo, self).save(*args, **kwargs)

class ProductsCategories(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class ProductsParameters(models.Model):
    product_info = models.ForeignKey(ProductInfo,on_delete=models.CASCADE,verbose_name='Информация о продукте')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметер')
    value = models.TextField(verbose_name='Значение',blank=True)


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
    shop = models.ForeignKey(Shop,verbose_name='Магазин',on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания')
    status = models.CharField(choices=OrderStatusChoice.choices,
                                default=OrderStatusChoice.NEW,
                                verbose_name='Статус')

class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name='Заказ',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Продукт',on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0)], verbose_name='Количество')