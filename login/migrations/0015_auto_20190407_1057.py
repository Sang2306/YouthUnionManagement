# Generated by Django 2.1.7 on 2019-04-07 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Role', verbose_name='Vai trò ID'),
        ),
    ]
