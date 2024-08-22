# serializers.py
from rest_framework import serializers
from .models import CustomUser, VehicleOwner, Vehicle, Mechanic, AutoRepairCompany, ServiceRequest, Appointment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class VehicleOwnerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = VehicleOwner
        fields = ['id', 'user', 'profile_picture', 'phone_number', 'address']

class VehicleSerializer(serializers.ModelSerializer):
    owner = VehicleOwnerSerializer()

    class Meta:
        model = Vehicle
        fields = ['id', 'owner', 'make', 'model', 'year', 'vin', 'current_status', 'warranty_info']

class MechanicSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Mechanic
        fields = ['id', 'user', 'phone_number', 'specialty', 'experience_years', 'profile_picture']

class AutoRepairCompanySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = AutoRepairCompany
        fields = ['id', 'user', 'name', 'address', 'phone_number', 'website']

class ServiceRequestSerializer(serializers.ModelSerializer):
    owner = VehicleOwnerSerializer()
    mechanic = MechanicSerializer()
    company = AutoRepairCompanySerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = ServiceRequest
        fields = ['id', 'owner', 'mechanic', 'company', 'vehicle', 'issue_description', 'service_type', 'status', 'created_at', 'updated_at', 'feedback']

class AppointmentSerializer(serializers.ModelSerializer):
    service_request = ServiceRequestSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'service_request', 'scheduled_date', 'location', 'confirmed']
