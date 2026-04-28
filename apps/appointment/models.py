# from django.db import models
# from apps.core.models import BaseModel


# class Appointment(BaseModel):

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     )
#     first_name = models.CharField(max_length=200, help_text="Client's name")
#     last_name = models.CharField(max_length=200, help_text="Client's last name")
#     date_of_birth = models.DateField(blank=True, null=True, help_text="Client's date of birth")
#     state = models.CharField(max_length=100, blank=True, null=True, help_text="Client's state of residence")
#     biological_sex = models.CharField(max_length=20, blank=True, null=True, help_text="Client's biological sex")
    
#     appointment_time = models.DateTimeField(help_text="Scheduled appointment date and time")
#     purpose = models.TextField(blank=True, null=True, help_text="Purpose of the appointment")
    
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='pending',
#         help_text="Appointment status"
#     )
    
#     note = models.TextField(blank=True, null=True, help_text="Additional notes about the appointment")

#     class Meta:
#         verbose_name = "Appointment"
#         verbose_name_plural = "Appointments"
#         ordering = ['-appointment_time']

#     def __str__(self):
#         return f"Appointment between {self.rep_name} and {self.client_name} on {self.appointment_time.strftime('%Y-%m-%d %H:%M')}"

#     @classmethod
#     def get_pending_appointments(cls):
#         return cls.objects.filter(status='pending')
