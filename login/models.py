from django.db import models
from datetime import datetime
# Create your models here.


class Role(models.Model):
    """
        Tao bang vai tro
    """
    role_ID = models.IntegerField(primary_key=True)
    role_name = models.CharField(
        verbose_name="Tên vai trò", max_length=100, default='')

    def __str__(self):
        return self.role_name


class Activity(models.Model):
    """
        Tao bang hoat dong
        moi user co the tham gia nhieu hoat dong,
        moi hoat dong co the duoc tham gia boi nhieu user
    """
    activity_ID = models.IntegerField(primary_key=True)
    name = models.CharField(verbose_name="Tên hoạt động", max_length=255)
    organizers = models.CharField(verbose_name="Ban tổ chức", max_length=512)
    start_date = models.DateTimeField(verbose_name="Ngày bắt đầu")
    # Chon nam hoc mac dinh
    school_year_default = str(datetime.now().year - 1) + \
        "-" + str(datetime.now().year)
    school_year = models.CharField(
        verbose_name="Năm học", max_length=50, default=school_year_default)
    description = models.TextField(verbose_name="Mô tả hoạt động")
    point = models.SmallIntegerField(verbose_name="Điểm")

    def __str__(self):
        return self.name


class User(models.Model):
    """
        Tao co so du lieu cho nguoi dung
    """
    #user co the co nhieu hoat dong va nguoc lai
    activities = models.ManyToManyField(Activity)
    user_ID = models.CharField(
        verbose_name="Sinh viên ID", max_length=12, primary_key=True)
    class_ID = models.CharField(verbose_name="Lớp ID", max_length=12)
    name = models.CharField(verbose_name="Tên", max_length=25)
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    role = models.ForeignKey(
        Role, verbose_name="Vai trò", on_delete=models.CASCADE)
    password = models.CharField(verbose_name="Mật khẩu", max_length=256)

    def __str__(self):
        return self.user_ID


class Mail(models.Model):
    """
        Tao co so du lieu luu tru mail cua nguoi dung
        each USER has many MAIl
        each MAIL has owned by one USER 
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail_address = models.EmailField(null=True)

    def __str__(self):
        return self.mail_address
