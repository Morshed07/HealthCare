# from django.db import models
# from apps.core.models import BaseModel
# from apps.doctor.models import Doctor
# from apps.service.models import Service
# from apps.consultation_type.models import ConsultationType


# class Appointment(BaseModel):

#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     )
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
#     consultation_type = models.ForeignKey(ConsultationType, on_delete=models.CASCADE, related_name='appointments')

#     first_name = models.CharField(max_length=200, help_text="Client's name")
#     last_name = models.CharField(max_length=200, help_text="Client's last name")
#     date_of_birth = models.DateField(blank=True, null=True, help_text="Client's date of birth")
#     state = models.CharField(max_length=100, blank=True, null=True, help_text="Client's state of residence")
#     biological_sex = models.CharField(max_length=20, blank=True, null=True, help_text="Client's biological sex")
#     email = models.EmailField(blank=True, null=True, help_text="Client's email address")
#     phone = models.CharField(max_length=20, blank=True, null=True, help_text="Client's phone number")
    
#     # Medical Information
#     reason_for_visit = models.TextField(blank=True, null=True, help_text="Reason for the visit")
#     current_medications = models.TextField(blank=True, null=True, help_text="Current medications")
#     known_allergies = models.TextField(blank=True, null=True, help_text="Known allergies")
#     medical_history = models.TextField(blank=True, null=True, help_text="Medical history")
    
#     appointment_time = models.DateTimeField(help_text="Scheduled appointment date and time")
    
#     # Payment
#     is_paid = models.BooleanField(default=False, help_text="Payment status")
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Appointment amount")
#     payment_method = models.CharField(max_length=155, help_text="Payment method")
    
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
#         return f"Appointment between {self.doctor.user.name} and {self.first_name + ' ' + self.last_name} on {self.appointment_time.strftime('%Y-%m-%d %H:%M')}"

#     @classmethod
#     def get_pending_appointments(cls):
#         return cls.objects.filter(status='pending')
