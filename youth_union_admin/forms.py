from django.forms import ModelForm, NumberInput, TextInput, DateTimeInput

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
            'start_date': DateTimeInput(attrs={'type': 'date'})
        }
