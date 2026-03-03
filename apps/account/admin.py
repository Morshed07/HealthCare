from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, ShippingAddress

# Register your models here.


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'representative_code', 'is_verified', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_verified', 'is_active', 'created_at')
    ordering = ('-created_at',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ModelAdmin):
    list_display = ('user', 'facility_name', 'city', 'state', 'zip_code', 'created_at')
    search_fields = ('user__email', 'facility_name', 'city', 'state', 'zip_code')
    list_filter = ('created_at',)
    ordering = ('-created_at',)