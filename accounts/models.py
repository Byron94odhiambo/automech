from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator







class CustomUser(AbstractUser):
    USER_ROLES = (
        ('owner', 'Vehicle Owner'),
        ('mechanic', 'Mechanic'),
        ('company', 'Auto Repair Company'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='owner')

    def __str__(self):
        return self.username
    

@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'owner':
            VehicleOwner.objects.create(user=instance)
        elif instance.role == 'mechanic':
            Mechanic.objects.create(user=instance)
        elif instance.role == 'company':
            AutoRepairCompany.objects.create(user=instance)
    
    
class VehicleOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Vehicle(models.Model):
    owner = models.ForeignKey(VehicleOwner, related_name='vehicles', on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    license_plate =models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=100, unique=True)  # Vehicle Identification Number
    current_status = models.CharField(max_length=255, blank=True, null=True)  # e.g., "In Service", "Available"
    warranty_info = models.CharField(max_length=255, blank=True, null=True)  # e.g., "2 years remaining"
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Mechanic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)  # E.g., Engine Specialist, Brake Specialist
    experience_years = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.user.username



class AutoRepairCompany(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    owner = models.ForeignKey(VehicleOwner, related_name='service_requests', on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, related_name='service_requests', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(AutoRepairCompany, related_name='service_requests', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, related_name='service_requests', on_delete=models.CASCADE)
    issue_description = models.TextField()
    service_type = models.CharField(max_length=100, blank=True, null=True)  # E.g., "Oil Change", "Brake Repair"
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the service from 1 to 5 stars"
    )

    def __str__(self):
        return f"Service Request for {self.vehicle} by {self.owner.user.username}"


class Appointment(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment for {self.service_request.vehicle} on {self.scheduled_date}"



