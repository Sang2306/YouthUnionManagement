from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/quan-tri-nguoi-dung/', consumers.ChangeConsumer),
]
