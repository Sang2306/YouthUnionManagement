# Generated by Django 2.1.7 on 2019-04-11 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0039_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='user',
        ),
        migrations.DeleteModel(
            name='Mail',
        ),
    ]
