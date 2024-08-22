from django.contrib import admin
from .models import CustomUser, VehicleOwner, Vehicle, Mechanic, AutoRepairCompany, ServiceRequest, Appointment
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Role',
            {
                'fields': (
                    'role',
                ),
            },
        ),
    )

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register additional models with the admin interface
@admin.register(VehicleOwner)
class VehicleOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')
    
    
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'year', 'vin')
    search_fields = ('make', 'model', 'vin')
    list_filter = ('year',)
    raw_id_fields = ('owner',) 

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'specialty', 'experience_years')
    search_fields = ('user__username', 'specialty')

@admin.register(AutoRepairCompany)
class AutoRepairCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'website')
    search_fields = ('name', 'phone_number', 'address')

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('owner', 'vehicle', 'mechanic', 'company', 'status', 'created_at')
    search_fields = ('owner__user__username', 'vehicle__make', 'vehicle__model')
    list_filter = ('status', 'created_at', 'updated_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'scheduled_date', 'location', 'confirmed')
    search_fields = ('service_request__vehicle__make', 'service_request__vehicle__model', 'location')
    list_filter = ('scheduled_date', 'confirmed')
