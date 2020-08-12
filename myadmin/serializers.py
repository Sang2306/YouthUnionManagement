from rest_framework import serializers
from django.contrib.auth import models
from login.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_ID', 'class_ID', 'name', 'date_of_birth', 'role', 'password', 'accumulated_point')
