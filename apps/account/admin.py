from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, EmailOTP

# Register your models here.


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'representative_code', 'is_verified', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_verified', 'is_active', 'created_at')
    ordering = ('-created_at',)

@admin.register(EmailOTP)
class EmailOTPAdmin(ModelAdmin):
    list_display = ('user', 'otp', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)