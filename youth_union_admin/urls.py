from django.urls import path, include

from youth_union_admin.views import (
    RoleView, delete_user, update_user, ActivityFormView, ActivityUpdateView, ActivityDetailView, upload_comment
)
from .views import UserView

app_name = 'youth_union_admin'

urlpatterns = [
    path('sinh-vien/', include([
        path('', UserView.as_view(), name='user-view'),
        path('xoa/', delete_user, name='delete-user'),
        path('cap-nhat/', update_user, name='update-user')
    ])),
    path('quan-ly-hoat-dong/', include([
        path('', ActivityFormView.as_view(), name='activity_form_view'),
        path('cap-nhat/<int:pk>', ActivityUpdateView.as_view(), name='activity_update_form'),
        path('xem-hoat-dong/<int:pk>', ActivityDetailView.as_view(), name='activity_detail_view')
    ])),
    path('vai-tro/them/', RoleView.as_view(), name='role-view'),
    path('phan-hoi/them/', upload_comment, name='add-comment')
]

api_urlpatterns = [

]

urlpatterns += api_urlpatterns
