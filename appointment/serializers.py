from rest_framework import serializers
from .models import Appointment
from app.models import Doctor
from rest_framework.exceptions import ValidationError
from datetime import datetime

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "date", "time", "phone_no", "caseInfo"]
        read_only_fields = ["status"]

    def validate(self, attrs):
        doctor = attrs.get("doctor")
        appointment_date = attrs.get("date")
        appointment_time = attrs.get("time")

        appointment_day = appointment_date.strftime('%A')
        print(doctor.get_days())
        if appointment_day not in doctor.get_days():
            raise ValidationError({"message": f"Doctor is not available on {appointment_day}"})

        if not (doctor.work_from <= appointment_time <= doctor.work_to):
            raise ValidationError({
                "message": f"Doctor is only available between {doctor.work_from.strftime('%H:%M')} and {doctor.work_to.strftime('%H:%M')} on {appointment_day}"
            })

        return attrs

    def create(self, validated_data):

        print(validated_data)
        appointment = Appointment.objects.create(
            patient=validated_data["patient"],
            doctor=validated_data["doctor"],
            date=validated_data["date"],
            time=validated_data["time"],
            phone_no=validated_data["phone_no"],
            caseInfo=validated_data["caseInfo"]
        )
        return appointment
    
    def get_doctor(self,obj):
        doctor = Doctor.objects.get(id=obj.doctor.id)
        return doctor.name
