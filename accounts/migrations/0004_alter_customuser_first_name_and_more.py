# Generated by Django 5.2 on 2025-05-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default='بدون نام', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='بدون نام', max_length=80),
            preserve_default=False,
        ),
    ]
