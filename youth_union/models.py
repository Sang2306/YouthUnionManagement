"""
    Cai dat cac bang trong co so du lieu
"""
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
from django.utils.timezone import now


class Role(models.Model):
    """
        Tao bang vai tro
    """
    role_ID = models.SmallIntegerField(primary_key=True)
    role_name = models.CharField(
        verbose_name="Tên vai trò", max_length=100, default='', unique=True)

    class Meta:
        db_table = 'youth_union_Role'
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
                          '-' + str(timezone.now().year)
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
    is_approved = models.BooleanField(default=False, help_text='Được user với quyền giáo viên approved!')

    class Meta:
        db_table = 'youth_union_Activity'
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


class User(models.Model):
    """
        Tao co so du lieu cho nguoi dung
    """
    # user co the co nhieu hoat dong
    activities = models.ManyToManyField(
        to=Activity, related_name='users_join_to', blank=True, editable=False)
    # user ( lop truong ) co the diem danh nhieu hoat dong
    checked_activities = models.ManyToManyField(
        Activity, related_name='was_checked_by',
        through='CheckActivity', through_fields=('user', 'activity'),
        editable=False
    )
    # Bình luận
    comments = models.ManyToManyField(
        to='Message', related_name='who_comments', through='Comment', through_fields=('user', 'message')
    )
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
        verbose_name="Điểm chuyên cần", default=60)

    class Meta:
        db_table = 'youth_union_User'
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def refresh_accumulated_point(self, school_year=str(timezone.now().year - 1) + '-' + str(timezone.now().year),
                                  school_semester=1):
        """
            Refresh lai diem cho user moi khi chon hoc ky khac,
            mac dinh la la hoc ky gan nhat
        """
        total = 0
        for activity in self.activities.all():
            if activity.school_year == school_year and activity.semester == school_semester:
                total += activity.point
        total = total if total <= 30 else 30
        self.accumulated_point += total

    def set_new_password(self, new_password):
        """
            Thiet lap mat khau khac neu nguoi dung doi mat khau
        """
        self.password = new_password

    def __lt__(self, other):
        return self.user_ID < other.user_ID

    def __str__(self):
        return self.user_ID


class CheckActivity(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activity = models.ForeignKey(to=Activity, on_delete=models.CASCADE)
    checked_date = models.DateField(auto_now_add=True, help_text='Ngày điểm danh')

    class Meta:
        db_table = 'youth_union_CheckActivity'
        verbose_name = 'Hoạt động đã điểm danh'
        verbose_name_plural = 'Hoạt động đã điểm danh'

    def __str__(self):
        return self.checked_date.strftime('%Y-%m-%d')


class Comment(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    message = models.ForeignKey(to='Message', on_delete=models.CASCADE)
    content = models.TextField(help_text='Nội dung bình luận')
    date_created = models.DateTimeField(auto_now_add=True, help_text='Ngày giờ bình luận')

    class Meta:
        db_table = 'youth_union_Comment'

    def __str__(self):
        return self.date_created.strftime('%Y-%m-%d')


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

    class Meta:
        db_table = 'youth_union_Mail'


# Upload pdf file
class UploadPdfFile(models.Model):
    """
        Model de luu file vao co so du lieu
    """
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, help_text='Ai đăng file thông báo')
    pdf_file = models.FileField(upload_to='announcements/', editable=False)

    def __str__(self):
        return self.pdf_file.name

    class Meta:
        db_table = 'youth_union_UploadPdfFile'


class Message(models.Model):
    """
        Các thông báo dành cho sinh viên
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text='Ai là nguời đăng thông báo?')
    title = models.CharField(max_length=1024, help_text='Tiêu đề thông báo')
    content = models.TextField(help_text='Nội dung thông báo')

    slug = models.SlugField(max_length=1024)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'youth_union_Message'
