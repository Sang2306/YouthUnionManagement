# Generated by Django 2.1.7 on 2019-04-18 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0049_auto_20190418_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='number_of_register',
            field=models.SmallIntegerField(default=0, editable=False, verbose_name='Số lượng dăng ký'),
        ),
    ]
