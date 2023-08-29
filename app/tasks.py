from backend.settings import EMAIL_ADDRESS
from django.core.mail import send_mail
from celery import shared_task
from app.models import Shop, Category, Product, \
    ProductInfo, Parameter
from backend.settings import SITE_DOMAIN

@shared_task
def send_thanks_for_ordering_email(email_address,order_id):
    send_mail(
        'Заказ принят',
        f'''Товары уже готовятся к отправке
        — мы пришлем уведомление в день доставки.
        Отслеживать статус заказа в реальном 
        времени можно по ссылке: http://{SITE_DOMAIN}/order/{order_id}''',
        EMAIL_ADDRESS,
        [email_address],
        fail_silently=False,
        )

@shared_task
def send_task_status_changed_email(email_address,order_id,status):
    send_mail(
        'Заказ принят',
        f'''Товары уже готовятся к отправке
        — мы пришлем уведомление в день доставки.
        Отслеживать статус заказа в реальном 
        времени можно по ссылке: http://{SITE_DOMAIN}/order/{order_id}''',
        EMAIL_ADDRESS,
        [email_address],
        fail_silently=False,
        )

@shared_task
def send_registration_confirmation_email(email_address,message):
    send_mail(
        'Подтверждение регистрации',
        'Для подтверждения регистрации вам необходимо перейти по ссылке:',
        EMAIL_ADDRESS,
        [email_address],
        fail_silently=False,
        )

@shared_task
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

