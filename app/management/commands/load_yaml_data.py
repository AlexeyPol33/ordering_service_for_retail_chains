from app.models import Shop, Category,Product,\
ProductInfo,Parameter,ProductParameter,Order,\
OrderItem,Contact, User
from django.core.management.base import BaseCommand, CommandParser
import yaml
import os


def db_dump(data:dict,filename:str) -> None:

    shop = Shop()
   

    shop.name = data['shop']
    #shop.url = ''
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
            



class Command(BaseCommand):
    help = 'Загружает данные из файла формата yaml'

    def handle(self, *args, **options):

        path = ''
        if options['path']:
            path = options['path']
            if not os.path.exists(path=path):
                self.stderr.write('Файл не существует')
            if not path[len(path)-5:] == '.yaml':
                self.stderr.write('Не верный формат файла')          
        else:
            list_files = os.listdir(path='.')
            for file in list_files:
                if file[len(file)-5:] == '.yaml':
                    path = file
                    break
        if len(path) == 0:
            self.stderr.write('Файл с расшерением yaml не найден')

        data = {}
        with open(path,'r',encoding='utf-8') as f:
            data = yaml.safe_load(f)

        try:
            db_dump(data,path)
            self.stdout.write(f'Файл {path} успешно загружен в базу данных')          
        except:
            self.stderr.write(f'Не удалось загрузить данные из файла {path}')
        
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            type=str,
            help='Задает путь'
            )
        parser.add_argument(
            '-u',
            '--user',
            type=str,
            help='Задает владельца магазина'
        )