from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'representative_code', 'is_verified', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_verified', 'is_active', 'created_at')
    ordering = ('-created_at',)