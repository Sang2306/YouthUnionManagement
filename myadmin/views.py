from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
# Create your views here.
def dashboards(request):
    return render(request, 'myadmin/base.html')

def user_list(request):
    return render(request, 'myadmin/user_list.html')

def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/myadmin/list')
    else:
        form = UserForm()
        return render(request, 'myadmin/create_user.html', {'form': form})
