import pytest
from app.models import Shop, Category,Product,\
ProductInfo,Parameter,ProductsParameters
from app.yaml_data_dump import db_dump

@pytest.fixture
def data_fixtur():
    data = {
        'shop': 'Связной', 
        'categories':[{
            'id': 1, 
            'name': 'Смартфоны'},], 
        'goods':[{
            'id': 1, 
            'category': 1, 
            'model': 'apple/iphone/xs-max', 
            'name': 'Смартфон Apple iPhone XS Max 512GB (золотистый)', 
            'price': 110000, 'price_rrc': 116990, 'quantity': 14, 
            'parameters': {
                'Диагональ (дюйм)': 6.5, 
                'Разрешение (пикс)': '2688x1242', 
                'Встроенная память (Гб)': 512,
                'Цвет': 'золотистый'
                }}]}
    return data

@pytest.mark.django_db
def test_db_dump(data_fixtur):
    db_dump(data_fixtur)
    assert Shop.objects.get(id=1).name == 'Связной'
    assert Category.objects.get(id=1).name == 'Смартфоны'
    assert Product.objects.get(id=1).name == 'Смартфон Apple iPhone XS Max 512GB (золотистый)'
    