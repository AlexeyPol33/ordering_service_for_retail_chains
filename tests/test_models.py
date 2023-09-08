import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from urllib.parse import quote
from django.test import override_settings, modify_settings
from rest_framework import serializers
import backend.settings as settings
from model_bakery import baker
from django.contrib.auth.hashers import check_password
from app.models import Shop, Category,Product,\
ProductInfo,Parameter,Order,\
OrderItem,Contact, User

@pytest.fixture
def user_factory():
    def factory(**kwargs):
        return baker.make('User',**kwargs)
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
def contact_item_factory():
    def factory(**kwargs):
        return baker.make('Contact',**kwargs)
    return factory

class TestUser:

    @pytest.fixture
    def correct_test_data(self,user_factory):
        users = []
        for i in range(1,4):
            user = user_factory(username=f'username{i}',
                                password=f'password{i}',
                                email=f'test@email{i}.com',
                                company=f'company{i}',
                                position=f'position{i}')
            users.append(user)
        return users

@pytest.mark.django_db
class TestShop:

    @pytest.fixture
    def correct_test_data(self,shop_factory):
        shops = []
        for i in range(1,4):
            shops.append(shop_factory(
                id = i,
                name = f'testname{i}',
                url = f'testurl{i}',
                ))
        return shops

    def test_create_shop(self,correct_test_data):
        shop = correct_test_data[0]

        assert isinstance(shop, Shop)
        assert shop.id == 1
        assert shop.name == 'testname1'
        assert shop.url == 'testurl1'

    def test_update_shop(self,correct_test_data):
        shop = correct_test_data[1]
        update_data = {'name':'testname_update',
                        'url':'testurl_update'}
        
        shop.name = update_data['name']
        shop.url = update_data['url']
        shop.save()
        update_shop = Shop.objects.get(id = shop.id)

        assert update_shop.name == update_data['name']
        assert update_shop.url == update_data['url']

    def test_shop_deletion(self, correct_test_data):
        shop = correct_test_data[2]
        shop.delete()
        with pytest.raises(Shop.DoesNotExist):
            Shop.objects.get(id=shop.id)

@pytest.mark.django_db
class TestCategory:

    @pytest.fixture
    def correct_test_data(self,category_factory,shop_factory):
        categorys = []
        for i in range(1,4):
            category = category_factory(name=f'testname{i}')
            categorys.append(category)
        return categorys
    
    def test_create_category(self,correct_test_data):
        category = correct_test_data[0]  
        assert category.name == 'testname1'


    def test_update_category(self,correct_test_data):
        category = correct_test_data[1]
        update_name = 'update_name'

        category.name = update_name
        category.save()
        update_category = Category.objects.get(id = category.id)
        assert update_category.name == update_name

    def test_category_deletion(self,correct_test_data):
        category = correct_test_data[0]
        category.delete()
        with pytest.raises(Category.DoesNotExist):
            Category.objects.get(id=category.id)

@pytest.mark.django_db
class TestProduct:

    @pytest.fixture
    def correct_test_data(self,product_factory,category_factory):
        products = []
        for i in range(1,4):
            category = category_factory(name=f'cname{i}')
            product = product_factory(name=f'pname{i}',categories=[category])
            products.append(product)
        return products

    def test_create_product(self,correct_test_data):
        pass

    def test_update_product(self, correct_test_data):
        pass

    def test_product_deletion(self,correct_test_data):
        pass

@pytest.mark.django_db
class TestProductInfo:

    @pytest.fixture
    def correct_test_data(self,product_info_factory,product_factory,shop_factory):
        products_info = []
        for i in range(1,4):
            product = product_factory(name=f'pname{i}')
            shop = shop_factory(name=f'sname{i}')
            product_info = product_info_factory(product=product,
                                                shop=shop,
                                                name=f'piname{i}',
                                                quantity=i,
                                                price=i,
                                                price_rrc=i)
            products_info.append(product_info)
        return products_info



    def test_create_product_info(self,correct_test_data):
        pass

    def test_update_product_info(self, correct_test_data):
        pass

    def test_product_info_deletion(self,correct_test_data):
        pass

@pytest.mark.django_db
class TestParameter:

    @pytest.fixture
    def correct_test_data(self,parameter_factory):
        parameters = []
        for i in range(1,4):
            parameter = parameter_factory(name=f'name{i}')
            parameters.append(parameter)
        return parameters

    def test_create_parameter(self,correct_test_data):
        pass

    def test_update_parameter(self, correct_test_data):
        pass

    def test_parameter_deletion(self,correct_test_data):
        pass

@pytest.mark.django_db
class TestOrder:

    @pytest.fixture
    def correct_test_data(self):
        pass

    def test_create_order(self,correct_test_data):
        pass

    def test_update_order(self, correct_test_data):
        pass

    def test_order_deletion(self,correct_test_data):
        pass

@pytest.mark.django_db
class TestOrderItem:

    @pytest.fixture
    def correct_test_data(self):
        pass

    def test_create_order_item(self,correct_test_data):
        pass

    def test_update_order_item(self, correct_test_data):
        pass

    def test_order_item_deletion(self,correct_test_data):
        pass

@pytest.mark.django_db
class TestContact:

    @pytest.fixture
    def correct_test_data(self):
        pass

    def test_create_contact(self,correct_test_data):
        pass

    def test_update_contact(self, correct_test_data):
        pass

    def test_contact_deletion(self,correct_test_data):
        pass












