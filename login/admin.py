from django.contrib import admin
from .models import User, UserAdmin, Mail, Role, Activity
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Mail)
admin.site.register(Role)
admin.site.register(Activity)
