# Generated by Django 5.2 on 2025-05-03 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_remove_order_phone_number_order_receiver_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(default='بدون کد', editable=False, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
