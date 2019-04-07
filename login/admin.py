from django.contrib import admin
from .models import User, Mail, Role, Activity
# Register your models here.
admin.site.register(User)
admin.site.register(Mail)
admin.site.register(Role)
admin.site.register(Activity)