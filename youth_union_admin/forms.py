from django.forms import ModelForm, NumberInput, TextInput

from youth_union.models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        widgets = {
            'role_ID': NumberInput(attrs={'class': 'form-control mx-1'}),
            'role_name': TextInput(attrs={'class': 'form-control mx-1'}),
        }
