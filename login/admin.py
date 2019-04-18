from django.contrib import admin
from .models import User, Mail, Role, Activity

# Tao fmodel quan tri User
class UserAdmin(admin.ModelAdmin):
    """
        Hien thi thong tin co ban cua user, va tim kiem thong tin user
    """
    search_fields = ["user_ID", ]
    ordering = ["user_ID", ]
    list_display = ['user_ID', "name", "password"]
    
# Tao model quan tri mail
class MailAdmin(admin.ModelAdmin):
    """
        Hien thi thong tin co ban cua mail VD user_ID, mail address
    """
    search_fields = ["mail_address", ]
    list_display = ["user_id", "mail_address"]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Role)
admin.site.register(Activity)
