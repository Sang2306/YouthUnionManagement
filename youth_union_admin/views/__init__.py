from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseGone
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import FormView, UpdateView

from youth_union.models import User, Role, Mail, Activity, Comment
from youth_union.views import get_user_from_session
from youth_union_admin.forms import RoleForm, ActivityForm


class UserView(View):

    def get(self, request, *args, **kwargs):
        # Bắt buộc phải đăng nhập mới có thể quản lý
        try:
            user_id = request.session.get('ID')
            user = User.objects.get(user_ID__iexact=user_id)
            # Không có quyền ban chấp hành đoàn
            if user.role_id != 3:
                raise KeyError
        except (ObjectDoesNotExist, KeyError):
            return HttpResponseRedirect(reverse('youth_union:login'))

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
            mail = Mail.objects.filter(mail_address=email)
            if mail.exists():
                return HttpResponse('<script>alert("Email đã tồn tại!"); location.reload();</script>')
            else:
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
    return JsonResponse(data={'status': 'Xóa thành công!'}, status=200)


@require_POST
def update_user(request):
    user_id = request.POST.get('user_id')
    class_id = request.POST.get('class_id')
    name = request.POST.get('name')
    date_of_birth = request.POST.get('date_of_birth')
    password = request.POST.get('password')
    role_id = request.POST.get('role_id')
    email = request.POST.get('email')

    user = User.objects.filter(user_ID=user_id)
    if user.exists():
        user.update(class_ID=class_id, name=name, date_of_birth=date_of_birth,
                    role_id=int(role_id), password=password)
        mail = Mail.objects.filter(user_id=user_id)
        if mail.exists():
            mail.update(mail_address=email)
        else:
            Mail.objects.create(user_id=user_id, mail_address=email)

    return redirect('youth_union_admin:user-view')


class ActivityFormView(FormView):
    http_method_names = ['get', 'post']
    form_class = ActivityForm
    template_name = 'youth_union_admin/sub/activity.html'

    def get_success_url(self):
        return reverse('youth_union_admin:activity_form_view')

    def get_context_data(self, **kwargs):
        form = super().get_form()
        context = super().get_context_data()
        context['form'] = form
        all_activities = Activity.objects.all()
        context['all_activities'] = all_activities
        return context

    def get(self, request, *args, **kwargs):
        # Bắt buộc phải đăng nhập mới có thể quản lý
        try:
            user_id = request.session.get('ID')
            user = User.objects.get(user_ID__iexact=user_id)
            # Không có quyền ban chấp hành đoàn
            if user.role_id != 3:
                raise KeyError
        except (ObjectDoesNotExist, KeyError):
            return HttpResponseRedirect(reverse('youth_union:login'))

        return super(ActivityFormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(ActivityFormView, self).form_valid(form)


class ActivityUpdateView(UpdateView):
    form_class = ActivityForm
    template_name = 'youth_union_admin/sub/activity_update.html'

    def get_queryset(self):
        return Activity.objects.all()

    def get_success_url(self):
        return reverse('youth_union_admin:activity_form_view')

    def form_valid(self, form):
        form.save()
        return super(ActivityUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        all_activities = Activity.objects.all()
        context['all_activities'] = all_activities
        return context


class ActivityDetailView(View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.filter(activity_ID=kwargs.get('pk')).first()
        if activity is None:
            return HttpResponseGone()
        rendered = render_to_string('youth_union_admin/modal/activity_detail.html', {'activity': activity})
        return JsonResponse(data={'rendered': rendered}, status=200)


@require_POST
def delete_activity(request, pk=None):
    the_activity = Activity.objects.filter(activity_ID=pk).first()
    if the_activity is not None:
        the_activity.delete()
    else:
        return JsonResponse(data={'status': 'Not found'}, status=404)
    return JsonResponse(data={'status': 'No content'}, status=204)


@require_POST
def upload_comment(request):
    user = get_user_from_session(request)
    message_id = request.POST.get('message_id')
    content = request.POST.get('content')
    Comment.objects.create(user=user, message_id=int(message_id), content=content)
    return JsonResponse(data={'status': 'created'}, status=201)


@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    Comment.objects.get(pk=comment_id).delete()
    return JsonResponse(data={'status': 'deleted'}, status=204)
