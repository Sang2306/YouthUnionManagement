from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from login.models import User
# Create your views here.


def home(request):
    """
        Neu du lieu nguoi dung chua co trong session thi chuyen huong sang trang dang nhap,
        nguoc lai lay thong tin dang nhap trong session
    """
    try:
        ID = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=ID)
        context = {
            'user': user,
        }
        return render(request, 'home/index.html', context)
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))
