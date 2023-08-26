from app.models import Shop, Category, Product, \
    ProductInfo, Parameter
from backend.settings import SITE_DOMAIN


def db_dump(data: dict, shop=None) -> Shop:

    if shop is None:
        shop, c = Shop.objects.get_or_create(name=data['shop'])

    shop.name = data['shop']

    shop.url = f"http://{SITE_DOMAIN}/api/shop/{shop.id}"
    shop.save()

    for c in data['categories']:
        category = Category()
        category.id = c['id']
        category.name = c['name']
        category.save()
        shop.categories.add(category)

    for g in data['goods']:
        product, c = Product.objects.get_or_create(id=g['id'])
        product.name = g['name']
        product.categories.add(Category.objects.get(id=g['category']))
        product.save()
        product_info, с = ProductInfo.objects.update_or_create(
            product=product,
            defaults={'quantity': g['quantity'],
                      'price': g['price'],
                      'price_rrc': g['price_rrc'],
                      'shop': shop})

        for p in g['parameters'].keys():

            parameter, c = Parameter.objects.get_or_create(
                name=p
            )
            product_info.add_parameter(
                parameter=parameter,
                value=g['parameters'][p]
                )
        product_info.save()
    return shop
