# Generated by Django 2.2.1 on 2020-07-11 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Tên hoạt động')),
                ('organizers', models.CharField(max_length=512, verbose_name='Ban tổ chức')),
                ('start_date', models.DateTimeField(verbose_name='Ngày bắt đầu')),
                ('school_year', models.CharField(default='2019-2020', max_length=50, verbose_name='Năm học')),
                ('semester', models.SmallIntegerField(choices=[(1, 'HỌC KỲ 1'), (2, 'HỌC KỲ 2')], verbose_name='Học kỳ')),
                ('description', models.TextField(verbose_name='Mô tả hoạt động')),
                ('point', models.SmallIntegerField(verbose_name='Điểm')),
                ('number_of_register', models.SmallIntegerField(default=0, editable=False, verbose_name='Số lượng dăng ký')),
            ],
            options={
                'verbose_name': 'Hoạt động',
                'verbose_name_plural': 'Hoạt động',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='CheckedActivity',
            fields=[
                ('activity_ID', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_ID', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(default='', max_length=100, unique=True, verbose_name='Tên vai trò')),
            ],
            options={
                'verbose_name': 'Vai trò',
                'verbose_name_plural': 'Vai trò',
            },
        ),
        migrations.CreateModel(
            name='UploadPdfFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(editable=False, upload_to='announcements/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ID', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Sinh viên ID')),
                ('class_ID', models.CharField(max_length=12, verbose_name='Lớp ID')),
                ('name', models.CharField(max_length=25, verbose_name='Tên')),
                ('date_of_birth', models.DateField(verbose_name='Ngày sinh')),
                ('password', models.CharField(max_length=256, verbose_name='Mật khẩu')),
                ('accumulated_point', models.IntegerField(default=60, verbose_name='Điểm chuyên cần')),
                ('activities', models.ManyToManyField(blank=True, editable=False, to='login.Activity')),
                ('checked_activities', models.ManyToManyField(editable=False, to='login.CheckedActivity')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Role', verbose_name='Vai trò')),
            ],
            options={
                'verbose_name': 'Người dùng',
                'verbose_name_plural': 'Người dùng',
            },
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_address', models.EmailField(default='a@b.com', max_length=254, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
        ),
    ]