from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from youth_union.models import User, Role, Mail
from youth_union.views import get_user_from_session
from youth_union_admin.forms import RoleForm


class UserView(View):

    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        users = User.objects.all()
        return render(request, 'youth_union_admin/sub/user.html', {'users': users, 'roles': roles})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        class_id = request.POST.get('class_id')
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        role_id = request.POST.get('role_id')
        email = request.POST.get('email')

        if user_id is None or class_id is None or name is None or date_of_birth is None or password is None:
            return HttpResponseBadRequest()

        try:
            user = User.objects.create(user_ID=user_id, class_ID=class_id,
                                       name=name, date_of_birth=date_of_birth,
                                       accumulated_point=65, password=password, role_id=role_id)
            Mail.objects.create(user=user, mail_address=email)
        except IntegrityError as ie:
            pass
        return redirect('youth_union_admin:user-view')


class RoleView(View):
    def get(self, request, *args, **kwargs):
        role_form = RoleForm()
        return render(request, 'youth_union_admin/sub/add_role.html', {'role_form': role_form})

    def post(self, request, *args, **kwargs):
        form_role = RoleForm(request.POST)
        if form_role.is_valid():
            form_role.save()
        return HttpResponse('<script>window.close();</script>')


@require_POST
def delete_user(request):
    user_id = request.POST.get('user_id')
    user = get_user_from_session(request)
    # User không phải là người thuộc ban chấp hành đoàn
    if user.role_id != 3:
        return JsonResponse(data={'status': 'Bạn không có quyền thực thi hành động này!'}, status=403)
    User.objects.get(user_ID=user_id).delete()
    return JsonResponse(data={'status': 'Xóa thành công!'}, status=204)


@require_POST
def update_user(request):
    user_id = request.POST.get('user_id')
    class_id = request.POST.get('class_id')
    name = request.POST.get('name')
    date_of_birth = request.POST.get('date_of_birth')
    password = request.POST.get('password')
    role_id = request.POST.get('role_id')
    email = request.POST.get('email')

    User.objects.filter(user_ID=user_id).update(class_ID=class_id, name=name, date_of_birth=date_of_birth,
                                                role_id=int(role_id), password=password)
    Mail.objects.filter(user_id=user_id).update(mail_address=email)
    return redirect('youth_union_admin:user-view')
