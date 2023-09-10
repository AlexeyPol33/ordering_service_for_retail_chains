import pytest
from django.core import mail
from model_bakery import baker
from rest_framework.test import APIClient
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.db import transaction
from django.test import TransactionTestCase
from django.test import TestCase
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
    categories = [None]
    for i in range(1,6):
        categories.append(category_factory(name=f'category{i}'))

    shops = [None]
    for i in range(1,6):
        shops.append(
            shop_factory(
                name=f'shop{i}',
                categories=[categories[i]]
                ))
        
    users = [None]
    for i in range(1,6):
        user = user_factory(
                username=f'username{i}',
                email=f'user{i}@email.com',
                )
        user.set_password(f'password{user.id}')
        user.is_active=True
        user.save()
        users.append(user)
        
    users_shop_owner = [None]
    for i in range(6,11):
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
    for i in range(11,16):
        user = user_factory(
                username=f'username{i}',
                email=f'user{i}@email.com',
                )
        user.set_password(f'password{user.id}')
        user.is_active=True
        user.save()
        users_buyers.append(user)
        
    contacts = [None]
    for i in range(1,6):
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
        
    parameters = [None]
    for i in range(1,6):
        parameters.append(parameter_factory(name=f'parameter{i}'))

    products = [None]
    for i in range(1,6):
        products.append(
            product_factory(
                categories=[categories[i]],
                name=f'product{i}',
                )
            )
        
    products_info = [None]
    for i in range(1,6):
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
    for i in range(1,6):
        orders.append(
            order_factory(
                user=users_buyers[i],
                shop=shops[i],
                )
        )

    order_items = [None]
    for i in range(1,6):
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

    def patch(self,correct_data_fixture):

        pass

@pytest.mark.django_db
class TestMakeShopOwner:
    pass

@pytest.mark.django_db
class TestPartnerUpdate:
    main_url = 'api/shop/upload/'

    def post(self,correct_data_fixture):
        pass

@pytest.mark.django_db
class TestProductView:
    main_url = 'api/product/'

    def get(self,correct_data_fixture):
        pass

    def post(self,correct_data_fixture):
        pass

    def patch(self,correct_data_fixture):
        pass

    def delete(self,correct_data_fixture):
        pass

@pytest.mark.django_db
class TestProductInfoView:
    main_url = 'api/productinfo/'

    def get(self):
        pass

    def patch(self):
        pass

@pytest.mark.django_db
class TestOrderView:
    main_url = 'api/order/'

    def get(self):
        pass

    def delete(self):
        pass

@pytest.mark.django_db
class TestOrderItemView:
    main_url = 'api/orderitem/'

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

@pytest.mark.django_db
class TestOrderConfirmation:
    main_url = 'api/order/confirm/'

    def post(self):
        pass

