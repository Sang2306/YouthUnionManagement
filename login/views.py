"""
    Cai dat cac views de xu ly request va hien thi cho nguoi dung
"""
import hashlib
import xlwt
import time
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import User, Activity, CheckedActivity, UploadPdfFile  # import cac models
from .form import UploadFileForm
# login view


def login(request):
    """
        Hien thi form dang nhap, neu nguoi dung dang nhap thanh cong
        Ghi lai thong tin dang nhap trong session neu nguoi dung chon 'Ghi nho'
    """
    context = {}
    try:
        # Neu trong session van con nguoi dung thi thong bao da dang nhap roi
        context = {
            'ID': request.POST['ID'],
            'password': request.POST['password'],
        }
        user = User.objects.get(user_ID__iexact=context['ID'])
        if user.password == context['password']:
            # Luu lai thong tin trong session truoc khi chuyen huong den trang chu
            save_session_data(request)
            return HttpResponseRedirect(reverse('home:home'))
        context['login_status'] = 'Sai mật khẩu'
    except MultiValueDictKeyError:
        pass
    except ObjectDoesNotExist:
        context['user_not_found'] = 'Người dùng không tồn tại'

    return render(request, 'login/login.html', context)


def save_session_data(request):
    """
        luu lai ID va password trong session de tranh dang nhap lai
    """
    request.session['ID'] = request.POST['ID']
    request.session['password'] = request.POST['password']


def clear_session_data(request):
    """
        Xoa du lieu luu trong session
        + Truong hop 1 nguoi dung logout
        + Truong hop 2 neu nguoi dung doi mat khau thi cung se dieu huong toi day
        trong request ma nguoi dung gui di co chua keyword newPwd voi gia tri la mat khau
    """
    try:
        new_password = request.POST['newPwd']
        user_id = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=user_id)
        user.set_new_password(new_password)
        user.save()
    except KeyError:
        pass
    request.session.flush()
    return HttpResponseRedirect(reverse('login:login'))


def activities(request):
    """
        Hien thi thong tin cac hoat dong chuan bi dien ra
        Neu du lieu nguoi dung chua co trong session thi chuyen huong sang trang dang nhap,
        nguoc lai lay thong tin dang nhap trong session
    """
    context = {}
    # hien thi thong tin nguoi dung dang nhap
    try:
        user_id = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=user_id)
        # kiem tra request de add hoac remove hoat dong cua user ../?status=rmo-22
        try:
            behaviour = request.POST['status'][:3]  # rmo - remove, add
            activity_id = request.POST['status'][4:]  # 22
            # Lay activty voi acttivity_ID trong request
            activity = Activity.objects.get(activity_ID=activity_id)
            if str(behaviour) == 'rmo':
                activity.number_of_register = F("number_of_register") - 1
                user.activities.remove(activity)
            else:
                activity.number_of_register = F("number_of_register") + 1
                user.activities.add(activity)
            # Luu lai thay doi gia tri number_of_register
            activity.save()
        except KeyError:
            pass
        context = {
            'user': user,
            'nowplustimedelta': timezone.now() + timezone.timedelta(days=3),
        }
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))
    # lay thong tin cac hoat dong trong co so du lieu va render vao tab hoat dong
    context['activities_list'] = Activity.objects.all()
    return render(request, 'login/activities.html', context)


class SemesterCodeError(Exception):
    """
        Exception cho viec nhap semester_code sai!
    """

    def __init__(self, message_string):
        super().__init__()
        self.message_string = message_string

    def __str__(self):
        return self.message_string


def personal(request):
    """
        hien thi thong tin cua nguoi dung so diem hien tai
    """
    context = {}
    # hien thi thong tin nguoi dung dang nhap
    semester_code = str(timezone.now().year-1) + '1'
    school_year = None
    school_semester = None
    activities_in_semester = []
    message_wrong_input = None
    try:
        user_id = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=user_id)
        try:
            # Lay semester code tu request
            semester_code = request.GET['semester']
            if len(semester_code) != 5:
                raise SemesterCodeError('Loi ma hoc ky khac 5 so')
        except SemesterCodeError:
            message_wrong_input = 'Không thể tìm thấy {}'.format(semester_code)
            semester_code = str(timezone.now().year-1) + '1'
        except KeyError:
            pass
        # chuyen doi semester_code thanh ten hoc ky
        school_year = int(semester_code[:4])  # 2019
        # rang buoc hoc ky phai thuoc hoc ky ma sinh vien bat dau vao truong -> tot nghiep
        begin_course = int(user_id[1:3])  # N16DCCNxxx -> 16
        begin_course = 2000+begin_course
        if school_year < begin_course or school_year > timezone.now().year:
            message_wrong_input = 'Không thể tìm thấy {}'.format(semester_code)
            semester_code = str(timezone.now().year-1) + '1'
            school_year = int(semester_code[:4])  # 2019

        school_year = str(school_year) + '-' + \
            str(school_year + 1)  # '2019-2020'
        school_semester = int(semester_code[-1:])
        for activity in user.activities.all():
            if activity.school_year == school_year and activity.semester == school_semester:
                activities_in_semester.append(activity)

        # tinh diem lai cho hoc ky hien tai dang chon
        user.refresh_accumulated_point(school_year, school_semester)
        context = {
            'user': user,
            # {{style}}="width: {{ user.accumulated_point }}%"
            'style': 'style',
            'activities_in_semester': activities_in_semester,
            'activities_in_semester_is_empty': activities_in_semester.__len__() == 0,
            'school_year': school_year,
            'school_semester': school_semester,
            'message_wrong_input': message_wrong_input,
            'hashed_user_pass': hashlib.sha512(user.password.encode()).hexdigest,
        }
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))

    return render(request, 'login/personal.html', context)


def check_attendance(request):
    """
        kiem tra su tham gia cua sinh vien,
        lop truong co quyen nay
    """
    context = {}
    # hien thi thong tin nguoi dung dang nhap
    try:
        user_id = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=user_id)
        choosed_activity = None
        members_registered = []
        try:
            activity_id = request.GET['activityID']
            choosed_activity = Activity.objects.get(activity_ID=activity_id)
            # loc danh sach sinh vien chung lop voi lop truong
            class_member = User.objects.filter(class_ID=user.class_ID)
            # loc danh sach sinh vien co dang ky tham gia hoat dong choosed_activity
            for member in class_member:
                if choosed_activity in member.activities.all():
                    members_registered.append(member)
        except KeyError:
            pass
        members_registered.sort()
        context = {
            'user': user,
            'members_registered': members_registered,
            'checked_activity_list': [
                # lay id cua cac hoat dong da diem danh
                act.activity_ID for act in user.checked_activities.all()
            ],
            # chi hien thi nut xac nhan neu co nguoi dung thuoc lop dang ky hoat dong
            'size_of_members_registered': members_registered.__len__(),
        }
        context['choosed_activity'] = choosed_activity
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))

    context['activities_list'] = Activity.objects.all()
    return render(request, 'login/check-attendance.html', context)


def confirm_check(request):
    """
        Xac nhan danh dach diem danh do check_attendance views chuyen huong den
    """
    # hien thi thong tin nguoi dung dang nhap
    try:
        user_id = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=user_id)
        choosed_activity = None
        members_registered = []
        try:
            activity_id = request.POST['activityID']
            try:
                # kiem tra trong CheckedActivity.objects da co id hoat dong nay chua
                # neu chua co thi raise exception ObjectDoesNotExist
                checked_activity = CheckedActivity.objects.get(pk=activity_id)
                user.checked_activities.add(checked_activity)
            except ObjectDoesNotExist:
                # tao mot record trong cac hoat dong da diem danh
                # luu lai
                # them record vao danh sach da diem danh cua nguoi dung
                checked_activity = CheckedActivity.objects.create(
                    activity_ID=activity_id)
                checked_activity.save()
                user.checked_activities.add(checked_activity)

            choosed_activity = Activity.objects.get(activity_ID=activity_id)
            # loc danh sach sinh vien chung lop voi lop truong
            class_member = User.objects.filter(class_ID=user.class_ID)
            # loc danh sach sinh vien co dang ky tham gia hoat dong choosed_activity
            for member in class_member:
                if choosed_activity in member.activities.all():
                    members_registered.append(member)
            # duyet danh sach dang ky neu request.POST[mssv] gay ra exception la khong co tham gia
            # nen ta se remove hoat dong khoi activities cua sinh vien
            for member in members_registered:
                try:
                    request.POST[member.user_ID]
                except KeyError:
                    member.activities.remove(choosed_activity)
        # them id hoat dong vao danh sach da diem danh
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('login:check-attendance'))
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))


def export_excel(request):
    """
        Xuat file excel du lieu diem ren luyen cua sinh vien do lop truong quan ly,
        Dua vao hoc ky de xuat du lieu.
    """
    # Thong tin hoc ky can trich xuat
    semester_code = None
    try:
        # Lay semester code tu request
        semester_code = request.GET['semester-code']
        if len(semester_code) != 5:
            raise SemesterCodeError('Loi ma hoc ky khac 5 so')
    except (SemesterCodeError, KeyError):
        return HttpResponse("<script> window.alert('Khong tim thay {}') </script>".format(semester_code))
        # chuyen doi semester_code thanh ten hoc ky
    school_year = int(semester_code[:4])  # 2019
    school_semester = int(semester_code[-1:])
    # Thong tin file excel
    wb = xlwt.Workbook(encoding='utf-8')
    ws = None
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    response = HttpResponse()
    response['content_type'] = 'application/ms-excel'
    file_name = '_report.xls'
    try:
        user_id = request.session.get('ID')
        # rang buoc hoc ky phai thuoc hoc ky ma sinh vien bat dau vao truong -> tot nghiep
        begin_course = int(user_id[1:3])  # N16DCCNxxx -> 16
        begin_course = 2000+begin_course
        if school_year < begin_course or school_year > timezone.now().year:
            return HttpResponse("<script> window.alert('Khong tim thay {}') </script>".format(semester_code))

        school_year = str(school_year) + '-' + \
            str(school_year + 1)  # '2019-2020'
        user = User.objects.get(user_ID__iexact=user_id)
        # Sheet Dxxxxxxx
        ws = wb.add_sheet('{}'.format(str(user.class_ID).upper()))
        # N16dccn130_report.xls
        file_name = user.class_ID.upper() + '_HK' + str(school_semester) + \
            '_' + school_year + file_name
        response['Content-Disposition'] = 'attachment; filename="{file_name}"'.format(
            file_name=file_name)
        columns = [
            'Tên sinh viên', 'MSSV', 'Điểm rèn luyện',
        ]
        # Ghi hang dau tien cua file excel la ten cac cot
        for col in enumerate(columns):
            ws.write(0, col[0], col[1], font_style)
        # loc danh sach sinh vien chung lop voi lop truong
        class_member = User.objects.filter(
            class_ID=user.class_ID).order_by('user_ID')
        # tinh diem cho sinh vien dua vao hoc ky (school_year, school_semester)
        row_num = 1
        for member in class_member:
            # Tinh diem dua vao hoc ky truoc khi xuat diem ra file excel
            member.refresh_accumulated_point(school_year, school_semester)
            # Ghi du lieu vao file
            ws.write(row_num, 0, str(member.name).upper())
            ws.write(row_num, 1, str(member.user_ID).upper())
            ws.write(row_num, 2, member.accumulated_point)
            row_num += 1

        wb.save(response)

    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))

    return response


def upload(request):
    ID = request.session.get('ID')
    user = User.objects.get(user_ID__iexact=ID)
    # Lay tat ca file pdf va hien thi
    all_files = UploadPdfFile.objects.all().order_by('-pdf_file')
    # Kiem tra form co hop le
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Tao doi tuong va luu file
            instance = UploadPdfFile(pdf_file=request.FILES['pdf_file'])
            instance.pdf_file.name = time.strftime('%Y-%m-%d') + '-' + instance.pdf_file.name
            instance.save()
            return HttpResponse('Successfully')
    else:
        form = UploadFileForm()

    context = {
        'user': user,
        'form': form,
        'all_files':all_files,
    }
    return render(request, 'login/upload.html', context)
