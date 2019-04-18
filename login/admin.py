from django.utils import timezone
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


# Tao model quan tri cho Activity
class ActivityAdmin(admin.ModelAdmin):
    """
        Hien thi thong tin cua hoat dong va tim kiem hoat dong dua vao thoi gian
    """
    search_fields = ["start_date"]
    ordering = ["start_date"]
    list_display = ["activity_ID", "name", "start_date",
                    "number_of_register", "get_number_of_joins"]

    def get_number_of_joins(self, obj):
        """
            Trả về số  lượng người tham gia
        """
        if obj.start_date < timezone.now():
            return len(obj.user_set.all())
        return '_'
    get_number_of_joins.short_description = "Số lượng tham dự"


# Register your models here.
admin.site.site_header = "Admin YouthPTIT"
admin.site.register(User, UserAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Role)
admin.site.register(Activity, ActivityAdmin)