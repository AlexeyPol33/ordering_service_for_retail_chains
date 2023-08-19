import pytest
from django.core import mail
from model_bakery import baker
from app.views import test_send_email
from rest_framework.test import APIClient
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from app.models import Shop, Category,Product,\
ProductInfo,Parameter,ProductParameter,Order,\
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
def product_parameter_factory():
    def factory(**kwargs):
        return baker.make('ProductParameter',**kwargs)
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
def contact_item_factory():
    def factory(**kwargs):
        return baker.make('Contact',**kwargs)
    return factory

#def test_email():
#    test_send_email()
#    print('Количество сообщений:',len(mail.outbox))
#    outbox = mail.outbox[0]
#    print('Заголовок:',outbox.subject)
#    print('Сообщение:',outbox.body)
#    print('От:',outbox.from_email)
#    print('Кому:',outbox.to)

def test_connection(api_client):
    response = api_client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
class TestUser:

    def test_registration(self,api_client):
        data = {'username':'username',
                'password':'password',
                'email':'test@email.com',
                'company':'company',
                'position':'position'}
        response = api_client.post('/api/user/',data)
        print(mail.outbox)
        print (response)
        token = api_client.post(
            '/api/token/',
            {
                'email':data['email'],
                'password':data['password'],
                }).json()['access']


        headers = {
            "Authorization": f"Bearer {token}"}
        
        response = api_client.get('/api/user/1/', headers=headers).json()

        
        assert response['id'] == 1
        assert response['username'] == 'username'
        assert check_password(data['password'],response['password'])

@pytest.mark.django_db
class TestBasket():
    @pytest.fixture
    def basket_fixtur(self,user_factory,
                      shop_factory,
                      category_factory,
                      product_factory,
                      product_info_factory):
        user = user_factory(
            username='username1',
            password='password1',
            email='test@email1.com',
            company='company1',
            position='position1')
        user.set_password('password1') # без этого не генерируется токен
        user.is_active = True # без этого не генерируется токен
        user.save()
        shop = shop_factory(
            name='shop1',
            url='url1',
            filename='filename1')
        category = category_factory(name = 'category')
        product = product_factory(
            id = 1,
            category = category,
            name = 'product1'
        )
        product_info = product_info_factory(
            product=product,
            shop=shop,
            name='Информация о product1',
            quantity=15,
            price=500,
            price_rrc=400
        )
        return {'user':user,'shop':shop,'product':product,}

    def test_make_basket(self,api_client,basket_fixtur):
        user = basket_fixtur['user']
        token = api_client.post(
            '/api/token/',
            {
                'email':user.email,
                'password':'password1',
                }).json()['access']
        headers = {
            "Authorization": f"Bearer {token}"}
        data = {'quantity':2,'product':1}
        print("product:", data['product'])
        response = api_client.post('/api/orderitem/',headers=headers,data=data).json()
        
        assert response['id'] == 1
        assert response['order'] == 1
        assert response['product'] == 1
        assert response ['quantity'] == 2

