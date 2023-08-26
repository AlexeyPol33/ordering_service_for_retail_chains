from django.contrib import admin
from app.models import Shop, Category, Product, \
    ProductInfo, Parameter, Order, \
    OrderItem, Contact, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'company_id', 'position', 'is_active',
        'last_login', 'is_superuser', 'first_name',
        'last_name', 'is_staff', 'date_joined'
        )

    list_filter = ('id', 'last_login', 'date_joined', 'is_active')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    list_per_page = 20
    readonly_fields = ('date_joined', 'last_login')
    actions_on_top = True
    actions_on_bottom = False


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'phone', 'country', 'region',
        'locality', 'street', 'house', 'description'
        )


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'get_categories')

    def get_categories(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_categories')

    def get_categories(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'shop', 'name',
        'get_parameters', 'quantity',
        'price', 'price_rrc')

    def get_parameters(self, obj):
        return ', '.join([parameter.name
                          for parameter in obj.parameters.all()])


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shop', 'dt', 'status')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')


admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
