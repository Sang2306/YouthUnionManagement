from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import UserForm
from login.models import User

from django.http import HttpResponse
# Create your views here.
def dashboards(request):
    return render(request, 'myadmin/index.html')

def user_list(request):
    userlist = User.objects.all()
    return render(request, 'myadmin/user_list.html', {'users': userlist})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm()

    return save_user_form(request, form, 'myadmin/includes/partial_create_user.html')
    

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




def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)




def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
    else:
        form = UserForm(instance=user)
    return save_user_form(request, form, 'myadmin/includes/partial_update_user.html')
