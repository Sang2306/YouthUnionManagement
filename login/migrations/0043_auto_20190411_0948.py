# Generated by Django 2.1.7 on 2019-04-11 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0042_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='semester',
            field=models.SmallIntegerField(choices=[(1, 'HỌC KỲ 1'), (2, 'HỌC KỲ 2')], verbose_name='Học kỳ'),
        ),
    ]