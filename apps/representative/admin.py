from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Representative

# Register your models here.


@admin.register(Representative)
class RepresentativeAdmin(ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'company', 'designation', 'representative_code', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'company', 'designation', 'representative_code')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)