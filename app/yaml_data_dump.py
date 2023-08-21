from app.models import Shop, Category,Product,\
ProductInfo,Parameter,ProductParameter
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def db_dump(data:dict,filename:str,shop=None) -> None:

    if shop == None:
        shop = Shop()

    shop.name = data['shop']
    current_site = get_current_site(HttpRequest())
    shop.url = f"http://{current_site.domain}/shop/{shop.id}"
    shop.filename = filename
    shop.save()

    for c in data['categories']:
        category = Category()
        category.id = c['id']
        category.name = c['name']
        category.shops == shop
        category.save()

    for g in data['goods']:
        product = Product()
        product.id = g['id']
        product.name = g['name']
        product.category = Category.objects.get(id=g['category'])
        product.save()
        product_info = ProductInfo() 
        product_info.product = product
        product_info.shop = shop
        product_info.name = g['name']
        product_info.quantity = g['quantity']
        product_info.price = g['price']
        product_info.price_rrc = g['price_rrc']
        product_info.save()
        for p in g['parameters'].keys():
            
            parameter = Parameter.objects.get_or_create(
                name = p
            )
            product_parameter = ProductParameter()
            product_parameter.product_info = product_info
            product_parameter.parameter = parameter[0]
            product_parameter.value = g['parameters'][p]
            

