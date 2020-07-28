from django.urls import path
from .views import create_user, user_list, dashboards

app_name = "admin"

urlpatterns = [
    path('', dashboards, name='dashboard'),
    path('create-user', create_user, name='create_user'),
    path('list-user', user_list, name='list_user'),
]