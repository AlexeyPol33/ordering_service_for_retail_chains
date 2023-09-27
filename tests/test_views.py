import pytest
import yaml
import time
from django.core import mail
from model_bakery import baker
from rest_framework.test import APIClient
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.db import transaction
from django.test import TransactionTestCase
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Shop, Category,Product,\
ProductInfo,Parameter,Order,\
OrderItem,Contact, User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return baker.make('app.User',**kwargs)
    return factory

@pytest.fixture
def shop_factory():
    def factory(**kwargs):
        return baker.make('Shop',**kwargs)
    return factory

@pytest.fixture
def category_factory():
    def factory(**kwargs):
        return baker.make('Category',**kwargs)
    return factory

@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product',**kwargs)
    return factory

@pytest.fixture
def product_info_factory():
    def factory(**kwargs):
        return baker.make('ProductInfo',**kwargs)
    return factory

@pytest.fixture
def parameter_factory():
    def factory(**kwargs):
        return baker.make('Parameter',**kwargs)
    return factory

@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order',**kwargs)
    return factory

@pytest.fixture
def order_item_factory():
    def factory(**kwargs):
        return baker.make('OrderItem',**kwargs)
    return factory

@pytest.fixture
def contact_factory():
    def factory(**kwargs):
        return baker.make('Contact',**kwargs)
    return factory

@pytest.fixture
def correct_data_fixture(category_factory,shop_factory,
                         user_factory,contact_factory,
                         parameter_factory,product_factory,
                         product_info_factory,order_factory,
                         order_item_factory):

    max_obj = 3

    categories = [None]
    for i in range(1,max_obj):
        categories.append(category_factory(name=f'category{i}'))

    shops = [None]
    for i in range(1,max_obj):
        shops.append(
            shop_factory(
                name=f'shop{i}',
                categories=[categories[i]]
                ))

    users = [None]
    for i in range(1,max_obj):
        user = user_factory(
                username=f'username{i}',
                email=f'user{i}@email.com',
                )
        user.set_password(f'password{user.id}')
        user.is_active=True
        user.save()
        users.append(user)
        
    users_shop_owner = [None]
    for i in range(max_obj,(max_obj*2)-1):
        user = user_factory(
                username=f'username{i}',
                email=f'user{i}@email.com',
                company=shops[i-5],
                position = User.UserPositionChoices.SHOP_OWNER
                )
        user.set_password(f'password{user.id}')
        user.is_active=True
        user.save()
        users_shop_owner.append(user)

    users_buyers = [None]
    for i in range((max_obj*2)-1,(max_obj*3)-2):
        user = user_factory(
                username=f'username{i}',
                email=f'user{i}@email.com',
                )
        user.set_password(f'password{user.id}')
        user.is_active=True
        user.save()
        users_buyers.append(user)

    contacts = [None]
    for i in range(1,max_obj):
        contacts.append(
            contact_factory(
                user=users[i],
                phone=f'+7777777777{i}',
                country=f'Country',
                region='Region',
                locality='Locality',
                street='street',
                house=f'{i}',
                ))

    for i in range(1,max_obj):
        contact_factory(
                user=users_buyers[i],
                phone=f'+7777777777{i}',
                country=f'Country',
                region='Region',
                locality='Locality',
                street='street',
                house=f'{i}',
                )
        
    parameters = [None]
    for i in range(1,max_obj):
        parameters.append(parameter_factory(name=f'parameter{i}'))

    products = [None]
    for i in range(1,max_obj):
        products.append(
            product_factory(
                categories=[categories[i]],
                name=f'product{i}',
                )
            )

    products_info = [None]
    for i in range(1,max_obj):
        products_info.append(
            product_info_factory(
                product=products[i],
                shop=shops[i],
                name=products[i].name,
                parameters=[parameters[i]],
                quantity = 100,
                price = 100,
                price_rrc = 100
            )
        )

    orders = [None]
    for i in range(1,max_obj):
        orders.append(
            order_factory(
                user=users_buyers[i],
                shop=shops[i],
                )
        )

    order_items = [None]
    for i in range(1,max_obj):
        order_items.append(
            order_item_factory(
                order=orders[i],
                product=products[i],
                quantity=1
            ))

    return {'categories':categories,'shops':shops,
            'users':users, 'users_shop_owner':users_shop_owner, 
            'users_buyers':users_buyers, 'contacts':contacts,
            'parameters':parameters, 'products':products,
            'products_info':products_info, 'orders':orders,
            'order_items':order_items}

def get_token(user):
    token = APIClient().post(
            '/api/token/',
            data={
                "email":user.email,
                "password":f"password{user.id}",
            },
            format='json').json()['access']
    return token

@pytest.mark.django_db
def test_connection(api_client):
    response = api_client.get('')
    assert response.status_code == 200

@pytest.mark.django_db
class TestUserViews:

    def test_registration(self,api_client):
        data = {'username':'username',
                'password':'password',
                'email':'test@email.com'
                }
        response = api_client.post('/api/user/',data,format='json')
        user = User.objects.get(id=response.json()['id'])
        user.is_active=True
        user.save()

        token = api_client.post(
            '/api/token/',
            data={
                "email":data['email'],
                "password":data['password']
                },
                format='json').json()['access']

        headers = {
            "Authorization": f"Bearer {token}"}

        response = api_client.get('/api/user/1/', headers=headers,format='json').json()

        assert response['id'] == 1
        assert response['username'] == 'username'

@pytest.mark.django_db
class TestContactView:
    main_url = '/api/user/contact/'

    def test_get(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users'][1]
        _contact = correct_data_fixture['contacts'][1]
        token = get_token(user)
        contact = api_client.get(
            path=self.main_url + f'{user.id}/',
            headers={"Authorization": f"Bearer {token}"},
            format='json')

        assert contact.status_code == 200

        contact = contact.json()
        assert _contact.user.id == contact['user']
        assert _contact.phone == contact['phone']
        assert _contact.country == contact['country']
        assert _contact.region == contact['region']
        assert _contact.locality == contact['locality']
        assert _contact.street == contact['street']
        assert _contact.house == contact['house']

    def test_patch(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users'][1]
        contact = Contact.objects.get(user=user)
        token = get_token(user)

        patch_data = {
            'phone':'+77777777888',
            'country':'newcountry',
            'region':'newregion',
            'locality':'newlocality',
            'street':'newstreet',
            'house':'newhouse'}
        response = api_client.patch(
            path=self.main_url + f'{contact.id}/',
            headers={"Authorization": f"Bearer {token}"},
            data=patch_data,
            format='json')

        contact = Contact.objects.get(user=user)

        assert response.status_code == 200
        assert contact.phone == patch_data['phone']
        assert contact.country == patch_data['country']
        assert contact.region == patch_data['region']
        assert contact.locality == patch_data['locality']
        assert contact.street == patch_data['street']
        assert contact.house == patch_data['house']

@pytest.mark.django_db
class TestShopView:
    main_url = '/api/shop/'

    def test_get(self,api_client,correct_data_fixture):
        shops = correct_data_fixture['shops']

        response = api_client.get(path=self.main_url).json()
        assert response['count'] == len(shops) - 1

        shop = shops[1]
        response = api_client.get(path=self.main_url + f'{shop.id}/').json()

        assert shop.id == response['id']
        assert shop.name == response['name']

    def test_patch(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_shop_owner'][1]
        token = get_token(user)
        shop = user.company
        data = {
            "name":"PatchName",
            "url":"https://PatchUrl.com",
            "categories":["PatchCategory1","PatchCategory2","PatchCategory3"]
        }

        response = api_client.patch(
            path=self.main_url + f'{shop.id}/',
            data=data,
            headers={"Authorization": f"Bearer {token}"},
            format='json'
            )
        shop = Shop.objects.get(id = shop.id)
        
        assert response.status_code == 200
        assert shop.name == data['name']
        assert shop.url == data['url']
        assert sorted([с.name for с in shop.categories.all()]) == sorted(data['categories'])


@pytest.mark.django_db
class TestMakeShopOwner:
    pass

@pytest.mark.django_db
class TestPartnerUpdate:
    main_url = '/api/shop/upload/'

    def test_post(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_shop_owner'][1]
        token = get_token(user)
        with open('shop1.yaml', 'r', encoding='utf-8') as f:
            upload_data = yaml.safe_load(f)

        response = api_client.post(
            path=self.main_url,
            headers={
                "Content-Disposition": 'attachment; filename=shop.yaml',
                "Authorization": f"Bearer {token}"},
            data={'file': upload_data}, 
            content_type='multipart/form-data')
        data = upload_data
        assert response.status_code == 201
        assert Shop.objects.get(id=user.company.id).name == data['shop']
        for catigory in data['categories']:
            assert Category.objects.get(id=catigory['id']).name == catigory['name']
        for g in data['goods']:
            product = Product.objects.get(id=g['id'])
            product_info = ProductInfo.objects.get(id=g['id'])
            assert product.id == g['id'] and product_info.id == g['id']
            assert sorted([c.id for c in product.categories.all()]) == sorted([g['category']])
            assert product.name == g['name']
            assert product_info.price == g['price']
            assert product_info.price_rrc == g['price_rrc']
            assert product_info.quantity == g['quantity']
            assert sorted([p.name for p in product_info.parameters.all()]) == sorted(g['parameters'].keys())

@pytest.mark.django_db
class TestProductView:
    main_url = '/api/product/'

    def test_get(self,api_client,correct_data_fixture):
        products = correct_data_fixture['products']
        product = products[1]

        request_all_products = api_client.get(path=self.main_url)
        request_one_product = api_client.get(path=self.main_url + f'{product.id}/')

        assert request_all_products.status_code == 200
        assert request_one_product.status_code == 200

        assert request_all_products.json()['count'] == len(products) - 1

        assert request_one_product.json()['id'] == product.id
        assert request_one_product.json()['name'] == product.name

    def test_post(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_shop_owner'][1]
        token = get_token(user)
        data = {
            "name":"TestName",
            "categories":["TestCategory1","TestCategory2","TestCategory3"]
        }

        response = api_client.post(
            path=self.main_url,
            data=data,
            headers={"Authorization": f"Bearer {token}"},
            format='json'
            )
        product = Product.objects.get(id=response.json()['id'])

        assert response.status_code == 201
        assert product.name == data['name']
        assert sorted([c.name for c in product.categories.all()]) == sorted(data['categories'])

    def test_patch(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_shop_owner'][1]
        shop = user.company
        product_info = ProductInfo.objects.filter(shop=shop).first()
        product = product_info.product
        token = get_token(user)
        data = {
            "name":"PathName",
            "categories":"TestAddCategory"}

        response = api_client.patch(
            path=self.main_url + f'{product.id}/',
            data=data,
            headers={"Authorization": f"Bearer {token}"},
            format='json'
            )
        product = Product.objects.get(id=product.id)

        assert response.status_code == 200
        assert product.name == data['name']
        assert data['categories'] in [c.name for c in product.categories.all()]


    def test_delete(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_shop_owner'][1]
        shop = user.company
        product_info = ProductInfo.objects.filter(shop=shop).first()
        product = product_info.product
        token = get_token(user)

        response = api_client.delete(
            path=self.main_url + f'{product.id}/',
            headers={"Authorization": f"Bearer {token}"},
            format='json'
            )
        
        assert response.status_code == 204
        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(id=product.id)


@pytest.mark.django_db
class TestProductInfoView:
    main_url = '/api/productinfo/'

    def test_get(self,api_client,correct_data_fixture):
        product_info = correct_data_fixture['products_info'][1]
        response = api_client.get(path=self.main_url+f'{product_info.id}/')

        assert response.status_code == 200

        response = response.json()

        assert response['id'] == product_info.id
        assert response['product'] == product_info.product.id
        assert response['shop'] == product_info.shop.id
        assert response['name'] == product_info.name
        assert response['quantity'] == ProductInfo.objects.get(id = product_info.id).quantity
        assert response['price'] == product_info.price
        assert response['price_rrc'] == product_info.price_rrc
        

    def test_patch(self,api_client,correct_data_fixture):

        pass

@pytest.mark.django_db
class TestOrderView:
    main_url = '/api/order/'

    def test_get(self,api_client,correct_data_fixture):
        order = correct_data_fixture['orders'][1]
        user = order.user
        token = get_token(user)

        response = api_client.get(
            path=self.main_url + f'{order.id}/',
            headers={"Authorization": f"Bearer {token}"},
            format='json')
        
        assert response.status_code == 200
        assert response.json()['id'] == order.id

    def test_delete(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_buyers'][1]
        order = Order.objects.filter(user=user).first()
        token = get_token(user)

        response = api_client.delete(
            path=self.main_url + f'{order.id}/',
            headers={"Authorization": f"Bearer {token}"},
            format='json'
        )

        assert response.status_code == 204
        with pytest.raises(Order.DoesNotExist):
            Order.objects.get(id=order.id)


@pytest.mark.django_db
class TestOrderItemView:
    main_url = '/api/orderitem/'

    def test_get(self,api_client,correct_data_fixture):
        order_items = correct_data_fixture['order_items']
        order_item = order_items[1]
        order = order_items[1].order
        user = order.user
        token = get_token(user)

        request_all_items = api_client.get(
            path=self.main_url,
            headers={"Authorization": f"Bearer {token}"},
            format='json'
        )
        request_item = api_client.get(
            path=self.main_url + f'{order_item.id}/',
            headers={"Authorization": f"Bearer {token}"},
            format='json'
        )

        assert request_all_items.status_code == 200
        assert request_item.status_code == 200

        request_all_items = request_all_items.json()
        request_item = request_item.json()

        assert request_all_items['count'] == 1
        assert request_item['order'] == order_item.id
        assert request_item['product'] == order_item.product.id
        assert request_item['quantity'] == order_item.quantity

    def test_post(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users'][1]
        product = correct_data_fixture['products'][1]
        token = get_token(user)
        data={
            "product":f"{product.id}",
            "quantity":1
        }
        response = api_client.post(
            path=self.main_url,
            headers={"Authorization": f"Bearer {token}"},
            data=data,
            format='json'
        )
        order_item = OrderItem.objects.get(id=response.json()['id'])

        assert response.status_code == 201
        assert order_item.product.id == int(data['product'])
        assert order_item.quantity == data['quantity']

    def test_delete(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_buyers'][1]
        order = Order.objects.filter(user=user).first()
        order_item = OrderItem.objects.filter(order=order).first()
        token = get_token(user)

        response = api_client.delete(
            path=self.main_url + f'{order_item.id}/',
            headers={"Authorization": f"Bearer {token}"})
        
        assert response.status_code == 204
        with pytest.raises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=order_item.id)


@pytest.mark.django_db
class TestOrderConfirmation:
    main_url = '/api/order/confirm/'

    def test_post(self,api_client,correct_data_fixture):
        user = correct_data_fixture['users_buyers'][1]
        token = get_token(user)
        response = api_client.post(
            path=self.main_url,
            headers={"Authorization": f"Bearer {token}"},
            content_type="application/json",)
        order = Order.objects.filter(user=user).first()
        assert response.status_code == 200
        assert order.status == Order.OrderStatusChoice.CONFIRMED
