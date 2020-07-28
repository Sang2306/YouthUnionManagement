from django import forms
from login.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_ID', 'class_ID', 'name', 'date_of_birth', 'role', 'password', 'accumulated_point')