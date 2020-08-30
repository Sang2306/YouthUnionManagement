from django.forms import ModelForm, NumberInput, TextInput, DateTimeInput, Textarea

from youth_union.models import Role, Activity


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'role_ID': NumberInput(attrs={'class': 'form-control mx-1'}),
            'role_name': TextInput(attrs={'class': 'form-control mx-1'}),
        }


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['is_approved']
        widgets = {
            'activity_ID': NumberInput(attrs={'class': 'form-control mx-1'}),
            'start_date': DateTimeInput(attrs={'class': 'form-control mx-1'}),
            'limit_register_day': NumberInput(
                attrs={'class': 'form-control mx-1', 'placeholder': 'Đóng đăng ký trước bao nhiều ngày?'}),
            'name': TextInput(attrs={'class': 'form-control mx-1'}),
            'description': Textarea(attrs={'class': 'form-control mx-1'}),
            'school_year': TextInput(attrs={'class': 'form-control mx-1'}),
            'organizers': TextInput(attrs={'class': 'form-control mx-1'}),
            'semester': TextInput(attrs={'class': 'form-control mx-1'}),
            'point': NumberInput(attrs={'class': 'form-control mx-1'}),
        }
