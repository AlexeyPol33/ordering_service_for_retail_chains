from django.contrib import admin
from app.models import Shop,ShopsCategories,Category,Product,\
ProductInfo,Parameter,ProductsParameters,Order,\
OrderItem,Contact, User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id','email','username','company_id','position','is_active',
        'last_login', 'is_superuser','first_name',
        'last_name','is_staff','date_joined'
        )
    
    list_filter = ('id','last_login','date_joined','is_active')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    list_per_page = 20
    readonly_fields = ('date_joined','last_login')
    actions_on_top = True
    actions_on_bottom = False


admin.site.register(User,UserAdmin)
admin.site.register(Contact)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(Parameter)
admin.site.register(Order)
admin.site.register(OrderItem)
