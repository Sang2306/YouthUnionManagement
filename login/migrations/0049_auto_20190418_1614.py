# Generated by Django 2.1.7 on 2019-04-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0048_activity_number_of_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='number_of_register',
            field=models.SmallIntegerField(default=0),
        ),
    ]
