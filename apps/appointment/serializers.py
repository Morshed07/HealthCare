from rest_framework import serializers
from .models import Appointment, AppointmentStatusHistory


class AppointmentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'service',
            'consultation_type',
            'appointment_time',
            'first_name',
            'last_name',
            'email',
            'phone',
            'reason_for_visit',
            'current_medications',
            'known_allergies',
            'medical_history',
            'date_of_birth',
            'state',
            'biological_sex',
            'payment_method',
            'amount',
            'status',
            'is_paid',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'status', 'is_paid', 'amount', 'created_at', 'updated_at'
        ]

    def get_amount(self, obj):
        return obj.consultation_type.fee

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
       

class AppointmentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatusHistory
        fields = [
            'id',
            'appointment',
            'status',
            'created_at',
        ]