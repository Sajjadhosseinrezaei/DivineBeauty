# Generated by Django 5.2 on 2025-04-22 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_slug_alter_product_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='lable',
            new_name='label',
        ),
    ]
