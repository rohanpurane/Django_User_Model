from django.contrib import admin
from .models import *
# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id','phone_number', 'email', 'otp', 'otp_expiry', 'max_otp_try', 'otp_max_out', 'is_active', 'is_staff', 'user_register_at')
admin.site.register(MyUser, MyUserAdmin)