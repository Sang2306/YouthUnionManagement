# Generated by Django 2.1.7 on 2019-04-05 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20190405_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('roleName', models.CharField(max_length=100)),
            ],
        ),
    ]
