from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ['id','doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    list_filter = ['id','doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    search_fields = ['id', 'doctor', 'service', 'consultation_type', 'appointment_time', 'status']
    ordering = ['-appointment_time']

