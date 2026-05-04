from rest_framework import serializers
from .models import Appointment, AppointmentStatusHistory
from apps.data.models import IntakeData
from apps.data.serializers import IntakeDataSerializer
from apps.service.models import Service


class AppointmentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    # Nested Serializer for the survey
    intake_form = IntakeDataSerializer(source='intake_data', required=False)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'service', 'consultation_type', 'appointment_time',
            'first_name', 'last_name', 'email', 'phone', 'reason_for_visit',
            'current_medications', 'known_allergies', 'medical_history',
            'date_of_birth', 'state', 'biological_sex', 'payment_method',
            'amount', 'status', 'is_paid', 'created_at', 'updated_at',
            'intake_form' # Added field
        ]
        read_only_fields = ['status', 'is_paid', 'amount', 'created_at', 'updated_at']

    def get_amount(self, obj):
        return obj.consultation_type.fee

    def validate(self, data):
        service = data.get('service')

        if service and not Service.objects.filter(pk=service.pk).exists():
            raise serializers.ValidationError({
                "service": "The selected service is not valid."
            })

        return data

    def create(self, validated_data):
        # Extract intake data from the main payload
        intake_data = validated_data.pop('intake_data', None)
        
        # Create appointment
        appointment = Appointment.objects.create(**validated_data)
        
        # Create intake form linked to the new appointment
        if intake_data:
            IntakeData.objects.create(appointment=appointment, **intake_data)
        
        return appointment
       

class AppointmentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatusHistory
        fields = [
            'id',
            'appointment',
            'status',
            'created_at',
        ]