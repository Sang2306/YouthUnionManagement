from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.urls import reverse

from login.models import User, UploadPdfFile
# Create your views here.


def home(request):
    """
        Neu du lieu nguoi dung chua co trong session thi chuyen huong sang trang dang nhap,
        nguoc lai lay thong tin dang nhap trong session
    """
    try:
        ID = request.session.get('ID')
        user = User.objects.get(user_ID__iexact=ID)
        # Lay tat ca file pdf va hien thi
        all_files = UploadPdfFile.objects.all().order_by('-pdf_file')
        # moi trang chi co 1 thong bao
        paginator = Paginator(all_files, 1)
        page = request.GET.get('page')
        announce = paginator.get_page(page)
        context = {
            'user': user,
            'announce': announce,
        }
        return render(request, 'home/index.html', context)
    except (ObjectDoesNotExist, KeyError):
        return HttpResponseRedirect(reverse('login:login'))
