from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import UserForm
from login.models import User
from django.http import HttpResponse, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import models
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .serializers import UserSerializer

class UserListCreate(ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.all()
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new User successful'
            }, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'message': 'Create a new User Unsuccessful'
            }, status=status.HTTP_400_BAD_REQUEST)

class UpdateDeleteUser(RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.all()

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, user_ID=kwargs.get('pk'))
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Update user successful'
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'message':'Update user unsucessful'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, user_ID=kwargs.get('pk'))
        user.delete()
        return JsonResponse({
            'message': 'Delete user successful!'
        }, status=status.HTTP_200_OK)

# ======== ^^^ On that API for ReactJS ^^^^=============

def login_myadmin(request):
    context = {}
    try:
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            save_session_data(request)
            return HttpResponseRedirect(reverse('myadmin:dashboard'))
        else:
            context['login-status'] = 'Sai mật khẩu'
    except MultiValueDictKeyError:
        pass
    except ObjectDoesNotExist:
        context['user_not_found'] = 'Người dùng khoonng tồn tại'
    return render(request, 'myadmin/login_myadmin.html', context)


@login_required(login_url='myadmin:login')
def save_session_data(request):
    request.session['name'] = request.POST['name']
    request.session['password'] = request.POST['password']
    request.session.set_expiry(60)




@login_required(login_url='myadmin:login')
def dashboards(request):
    return render(request, 'myadmin/index.html')
    
        
        

@login_required(login_url='myadmin:login')
def user_list(request):
    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 2)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'myadmin/user_list.html', { 'users': users })


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm()

    return save_user_form(request, form, 'myadmin/includes/partial_create_user.html')
    
@login_required(login_url='myadmin:login')
def save_user_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            users = User.objects.all()
            data['html_user_list'] = render_to_string('myadmin/includes/partial_user_list.html', {
                'users': users
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='myadmin:login')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        user.delete()
        data['form_is_valid'] = True
        users = User.objects.all()
        data['html_user_list'] = render_to_string('myadmin/includes/partial_user_list.html', {
            'users': users
        })
    else:
        context = {'user': user}
        data['html_form'] = render_to_string('myadmin/includes/partial_delete_user.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='myadmin:login')
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
    else:
        form = UserForm(instance=user)
    return save_user_form(request, form, 'myadmin/includes/partial_update_user.html')

