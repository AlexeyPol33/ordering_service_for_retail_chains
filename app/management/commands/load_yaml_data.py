from app.models import User
from django.core.management.base import BaseCommand
from app.yaml_data_dump import db_dump
import yaml
import os


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
        user = None
        if options['user']:
            try:
                user = User.objects.get(id=options['user'])
            except Exception:
                self.stderr.write('Пользователь не найден')

        data = {}
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        try:
            shop = db_dump(data)
            if user:
                user.company = shop
                user.position = User.UserPositionChoices.SHOP_OWNER
                user.save()
            self.stdout.write(f'Файл {path} успешно загружен в базу данных')
        except Exception as e:
            self.stderr.write(f'Не удалось загрузить данные\
                                из файла {path}, ошибка {e}')

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
            type=int,
            help='Задает владельца магазина,\
                  нужно указать id пользователя\
                      в качестве аргумента'
        )
