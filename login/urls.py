from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login, name='login'),
    path('activities/', views.activities, name='activities'),
    path('exit/', views.clear_session_data, name='exit'),
    path('personal/', views.personal, name='personal'),
    path('check-attendance/', views.check_attendance, name='check-attendance'),
    path('confirm-check/', views.confirm_check, name='confirm-check')
]
