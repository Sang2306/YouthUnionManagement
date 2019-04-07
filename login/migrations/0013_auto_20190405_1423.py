# Generated by Django 2.1.7 on 2019-04-05 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_auto_20190405_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='class_ID',
            field=models.CharField(max_length=12, verbose_name='Lớp ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=25, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256, verbose_name='Mật khẩu'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role_ID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.Role', verbose_name='Vai trò ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_ID',
            field=models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Sinh viên ID'),
        ),
    ]
