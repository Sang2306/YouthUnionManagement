# Generated by Django 2.1.7 on 2019-04-10 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0032_auto_20190410_1352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkedactivity',
            old_name='acitvity',
            new_name='acitvities',
        ),
        migrations.RenameField(
            model_name='checkedactivity',
            old_name='user',
            new_name='users',
        ),
    ]
