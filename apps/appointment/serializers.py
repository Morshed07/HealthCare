from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status', 'is_paid', 'amount']

    def validate(self, data):
        doctor = data.get('doctor')
        appointment_time = data.get('appointment_time')
        service = data.get('service')

        # 1. Check Availability: See if doctor is already booked at that time
        if Appointment.objects.filter(doctor=doctor, appointment_time=appointment_time).exists():
            raise serializers.ValidationError({
                "appointment_time": "This time slot is already booked for this doctor."
            })

        # 2. Logic Check: Ensure doctor provides this specific service
        # (Assuming your Doctor model has a 'services' M2M field)
        if service not in doctor.services.all():
            raise serializers.ValidationError({
                "service": f"Dr. {doctor.name} does not offer the {service.name} service."
            })

        return data