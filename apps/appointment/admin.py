from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ['doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    list_filter = ['doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    search_fields = ['doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    ordering = ['-appointment_time']

