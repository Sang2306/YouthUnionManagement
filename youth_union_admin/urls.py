from django.urls import path, include

from youth_union_admin.views import RoleView, delete_user, update_user
from .views import UserView

app_name = 'youth_union_admin'

urlpatterns = [
    path('sinh-vien/', include([
        path('', UserView.as_view(), name='user-view'),
        path('xoa/', delete_user, name='delete-user'),
        path('cap-nhat/', update_user, name='update-user')
    ])),
    path('vai-tro/them/', RoleView.as_view(), name='role-view')
]