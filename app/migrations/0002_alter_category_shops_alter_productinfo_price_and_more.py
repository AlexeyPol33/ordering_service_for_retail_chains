# Generated by Django 4.2.3 on 2023-08-01 06:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='shops',
            field=models.ManyToManyField(blank=True, through='app.Shops_Categories', to='app.shop'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='quantity',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='filename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название файла'),
        ),
    ]
