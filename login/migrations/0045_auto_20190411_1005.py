# Generated by Django 2.1.7 on 2019-04-11 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0044_auto_20190411_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_ID',
            field=models.SmallIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Tên vai trò'),
        ),
    ]