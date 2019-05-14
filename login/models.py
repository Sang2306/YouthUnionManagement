"""
    Cai dat cac bang trong co so du lieu
"""
from django.db import models
from django.utils import timezone
# Create your models here.


class Role(models.Model):
    """
        Tao bang vai tro
    """
    role_ID = models.SmallIntegerField(primary_key=True)
    role_name = models.CharField(
        verbose_name="Tên vai trò", max_length=100, default='', unique=True)

    class Meta:
        verbose_name = "Vai trò"
        verbose_name_plural = "Vai trò"

    def __str__(self):
        return self.role_name


class Activity(models.Model):
    """
        Tao bang hoat dong
        moi user co the tham gia nhieu hoat dong,
        moi hoat dong co the duoc tham gia boi nhieu user
    """
    activity_ID = models.IntegerField(primary_key=True)
    name = models.CharField(verbose_name="Tên hoạt động",
                            max_length=255, unique=True)
    organizers = models.CharField(verbose_name="Ban tổ chức", max_length=512)
    start_date = models.DateTimeField(verbose_name="Ngày bắt đầu")
    # nam hoc mac dinh gan nhat 2018-2019 hien tai
    school_year_default = str(timezone.now().year - 1) + \
        "-" + str(timezone.now().year)
    school_year = models.CharField(
        verbose_name="Năm học", max_length=50, default=school_year_default)
    # hoc ky
    SEMESTER_1, SEMESTER_2 = 1, 2
    SEMESTER_IN_SCHOOL = (
        (SEMESTER_1, 'HỌC KỲ 1'),
        (SEMESTER_2, 'HỌC KỲ 2'),
    )
    semester = models.SmallIntegerField(
        verbose_name="Học kỳ", choices=SEMESTER_IN_SCHOOL)
    description = models.TextField(verbose_name="Mô tả hoạt động")
    point = models.SmallIntegerField(verbose_name="Điểm")

    # So luong nguoi dang ky tham gia
    number_of_register = models.SmallIntegerField(
        verbose_name="Số lượng dăng ký", default=0, editable=False)

    class Meta:
        verbose_name = "Hoạt động"
        verbose_name_plural = "Hoạt động"
        ordering = ["start_date"]

    def is_opening(self):
        """
            tra ve True neu hoat dong nay chua, hoac dang dien ra, nguoc lai False
        """
        now = timezone.now()
        return self.start_date.date() >= now.date()

    def __str__(self):
        return self.name


class CheckedActivity(models.Model):
    """
        cac hoat dong da duoc nguoi dung( lop truong ) diem danh
    """
    activity_ID = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.activity_ID)


class User(models.Model):
    """
        Tao co so du lieu cho nguoi dung
    """
    # user co the co nhieu hoat dong
    activities = models.ManyToManyField(Activity, blank=True, editable=False)
    # user ( lop truong ) co the diem danh nhieu hoat dong
    checked_activities = models.ManyToManyField(
        CheckedActivity, editable=False)
    # Cac cot khac cua User table
    user_ID = models.CharField(
        verbose_name="Sinh viên ID", max_length=12, primary_key=True)
    class_ID = models.CharField(verbose_name="Lớp ID", max_length=12)
    name = models.CharField(verbose_name="Tên", max_length=25)
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    role = models.ForeignKey(
        Role, verbose_name="Vai trò", on_delete=models.CASCADE)
    password = models.CharField(verbose_name="Mật khẩu", max_length=256)
    # muc diem chuyen can mac dinh = 69
    accumulated_point = models.IntegerField(
        verbose_name="Điểm chuyên cần", default=69)

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def refresh_accumulated_point(self, school_year=str(timezone.now().year - 1) +
                                  "-" + str(timezone.now().year), school_semester=1):
        """
            Refresh lai diem cho user moi khi chon hoc ky khac,
            mac dinh la la hoc ky gan nhat
        """
        for activity in self.activities.all():
            if activity.school_year == school_year and activity.semester == school_semester:
                self.accumulated_point += activity.point

    def set_new_password(self, new_password):
        """
            Thiet lap mat khau khac neu nguoi dung doi mat khau
        """
        self.password = new_password

    def __lt__(self, other):
        return self.user_ID < other.user_ID

    def __str__(self):
        return self.user_ID


class Mail(models.Model):
    """
        Tao co so du lieu luu tru mail cua nguoi dung
        each USER has many MAIl
        each MAIL has owned by one USER
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail_address = models.EmailField(
        unique=True, default='a@b.com')

    def __str__(self):
        return self.mail_address

# Upload pdf file
class UploadPdfFile(models.Model):
    """
        Model de luu file vao co so du lieu
    """
    pdf_file = models.FileField(upload_to='announcements/', editable=False)
    
    def __str__(self):
        return self.pdf_file.name
