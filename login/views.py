from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Activity, Role  # import cac models
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

ACTIVITIES_LIST = Activity.objects.all() #tap cac hoat dong co trong co so du lieu
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
            behaviour = request.GET['status'][:3]  # rmo - remove, add
            acttivityID = request.GET['status'][4:]  # 22
            # Lay activty voi acttivity_ID trong request
            activity = Activity.objects.get(activity_ID=acttivityID)
            if str(behaviour) == 'rmo':
                user.activities.remove(activity)
            else:
                user.activities.add(activity)
        except KeyError:
            pass
        context = {
            'user': user,
            'nowplustimedelta' : timezone.now() + timezone.timedelta(days=3),
        }
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))
    # lay thong tin cac hoat dong trong co so du lieu va render vao tab hoat dong
    context['activities_list'] = ACTIVITIES_LIST
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
        context = {
            'user': user,
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
        context = {
            'user': user,
        }
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))

    return render(request, 'login/check_attendance.html', context)