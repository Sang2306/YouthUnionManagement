from django.urls import path
from . import views

app_name = "myadmin"

urlpatterns = [
    path('', views.dashboards, name='dashboard'),
    path('login', views.login_myadmin, name='login'),
    path('list-user/', views.user_list, name='list_user'),
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/<int:pk>', views.update_user, name='update_user'),
    path('delete-user/<int:pk>', views.delete_user, name='delete_user'),

    path('api/user', views.UserListCreate.as_view()),
    path('api/user/<int:pk>', views.UpdateDeleteUser.as_view()),
]