# Generated by Django 4.2.3 on 2023-08-06 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_product_info_productparameter_product_info_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Shops_Categories',
            new_name='ShopsCategories',
        ),
    ]
