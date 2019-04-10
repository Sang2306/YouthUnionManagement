from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Activity, CheckedActivity  # import cac models
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
        user = User.objects.get(user_ID=context['ID'])
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
    """
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
        ID = request.session.get('ID')
        user = User.objects.get(user_ID=ID)
        # kiem tra request de add hoac remove hoat dong cua user ../?status=rmo-22
        try:
            behaviour = request.POST['status'][:3]  # rmo - remove, add
            activityID = request.POST['status'][4:]  # 22
            # Lay activty voi acttivity_ID trong request
            activity = Activity.objects.get(activity_ID=activityID)
            if str(behaviour) == 'rmo':
                user.activities.remove(activity)
            else:
                user.activities.add(activity)
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


def personal(request):
    """
        hien thi thong tin cua nguoi dung so diem hien tai
    """
    context = {}
    # hien thi thong tin nguoi dung dang nhap
    try:
        ID = request.session.get('ID')
        user = User.objects.get(user_ID=ID)
        user.refresh_accumulated_point()
        context = {
            'user': user,
            # {{style}}="width: {{ user.accumulated_point }}%"
            'style': 'style',
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
        ID = request.session.get('ID')
        user = User.objects.get(user_ID=ID)
        choosed_activity = None
        members_registered = []
        try:
            activityID = request.GET['activityID']
            choosed_activity = Activity.objects.get(activity_ID=activityID)
            # loc danh sach sinh vien chung lop voi lop truong
            class_member = User.objects.filter(class_ID=user.class_ID)
            # loc danh sach sinh vien co dang ky tham gia hoat dong choosed_activity
            for member in class_member:
                if choosed_activity in member.activities.all():
                    members_registered.append(member)
        except KeyError:
            pass
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
        ID = request.session.get('ID')
        user = User.objects.get(user_ID=ID)
        choosed_activity = None
        members_registered = []
        try:
            activityID = request.POST['activityID']
            try:
                # kiem tra trong CheckedActivity.objects da co id hoat dong nay chua
                # neu chua co thi raise exception ObjectDoesNotExist
                checked_activity = CheckedActivity.objects.get(pk=activityID)
                user.checked_activities.add(checked_activity)
            except ObjectDoesNotExist:
                # tao mot record trong cac hoat dong da diem danh
                # luu lai
                # them record vao danh sach da diem danh cua nguoi dung
                checked_activity = CheckedActivity.objects.create(
                    activity_ID=activityID)
                checked_activity.save()
                user.checked_activities.add(checked_activity)

            choosed_activity = Activity.objects.get(activity_ID=activityID)
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
