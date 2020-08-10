from django.urls import path
from . import views

app_name = 'youth_union'

urlpatterns = [
    path('', views.login, name='login'),
    path('hoat-dong/', views.activities, name='activities'),
    path('export-xls/', views.export_excel, name='export-xls'),
    path('exit/', views.clear_session_data, name='exit'),
    path('ca-nhan/', views.personal, name='personal'),
    path('check-attendance/', views.check_attendance, name='check-attendance'),
    path('confirm-check/', views.confirm_check, name='confirm-check'),
    path('tai-len/', views.upload, name='upload'),
]
