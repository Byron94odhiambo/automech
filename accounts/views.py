from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm  # Create this form based on your CustomUser model
from django.contrib.auth.decorators import login_required
from .models import VehicleOwner, Vehicle, ServiceRequest, Appointment
from .forms import VehicleOwnerProfileForm,MechanicSearchForm, VehicleForm, ServiceAppointmentForm,VehicleOwnerProfileUpdateForm, ServiceRequestForm,ServiceRequestStatusForm,FeedbackForm,MechanicProfileUpdateForm, UserProfileUpdateForm, ProfilePictureUpdateForm
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.utils import timezone
from .serializers import CustomUserSerializer, VehicleOwnerSerializer, VehicleSerializer, MechanicSerializer, AutoRepairCompanySerializer, ServiceRequestSerializer, AppointmentSerializer
from rest_framework import generics
from .models import CustomUser, VehicleOwner, Vehicle, Mechanic, AutoRepairCompany, ServiceRequest, Appointment



def landing_page(request):
    return render(request, 'dashboards/landing.html')


#Register users to our webapp then redirect to their respective dashboards
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect based on user role
            if user.role == 'owner':
                return redirect('owner_dashboard')
            elif user.role == 'mechanic':
                return redirect('mechanic_dashboard')
            elif user.role == 'company':
                return redirect('company_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# Authenticate users to their account
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to profile setup if the user is a vehicle owner and hasn't set up their profile yet
            if user.role == 'owner':
                return redirect('owner_dashboard')
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')
#Redirect user to their respective dashboard
@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'owner':
        return redirect('owner_dashboard')
    elif user.role == 'mechanic':
        return redirect('mechanic_dashboard')
    elif user.role == 'company':
        return redirect('company_dashboard')
#Give vehicle owners capability of setting up their profile
@login_required
def setup_profile(request):
    try:
        vehicle_owner = request.user.vehicleowner
    except VehicleOwner.DoesNotExist:
        vehicle_owner = VehicleOwner(user=request.user)
        vehicle_owner.save()

    if vehicle_owner.phone_number and vehicle_owner.address:
        return redirect('owner_dashboard')  # Redirect to the dashboard if the profile is already set up

    if request.method == 'POST':
        profile_form = VehicleOwnerProfileForm(request.POST, request.FILES, instance=vehicle_owner)
        vehicle_form = VehicleForm(request.POST)
        if profile_form.is_valid() and vehicle_form.is_valid():
            profile_form.save()
            vehicle = vehicle_form.save(commit=False)
            vehicle.owner = vehicle_owner
            vehicle.save()
            return redirect('owner_dashboard')  # Redirect to the dashboard after saving
    else:
        profile_form = VehicleOwnerProfileForm(instance=vehicle_owner)
        vehicle_form = VehicleForm()

    return render(request, 'profile_setup/setup_profile.html', {
        'profile_form': profile_form,
        'vehicle_form': vehicle_form
    })
# Vehicle owners can update profile
@login_required
def update_profile(request):
    vehicle_owner = request.user.vehicleowner

    if request.method == 'POST':
        form = VehicleOwnerProfileUpdateForm(request.POST, request.FILES, instance=vehicle_owner)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = VehicleOwnerProfileUpdateForm(instance=vehicle_owner)

    return render(request, 'owner/update_profile.html', {'form': form})
# Vehicle owners can add vehicle
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user.vehicleowner
            vehicle.save()
            return redirect('owner_dashboard')
    else:
        form = VehicleForm()
    return render(request, 'owner/add_vehicle.html', {'form': form})
#Vehicle owners can view list of vehicles
@login_required
def vehicle_list(request):
    # Fetch vehicles for the logged-in vehicle owner
    vehicles = request.user.vehicleowner.vehicles.all()
    return render(request, 'owner/vehicle_list.html', {'vehicles': vehicles})
#Vehicle owners can edit vehicle details
@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user.vehicleowner)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'owner/edit_vehicle.html', {'form': form, 'vehicle': vehicle})

#Delete vehicle
@login_required
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user.vehicleowner)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return redirect('vehicle_detail', vehicle_id=vehicle.id)



#Vehicle owners can view vehicle details    
@login_required
def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user.vehicleowner)
    service_history = ServiceRequest.objects.filter(vehicle=vehicle).order_by('-created_at')
    completed_services = ServiceRequest.objects.filter(vehicle=vehicle, status='completed').order_by('-created_at')
    
    context = {
        'vehicle': vehicle,
        'service_history': service_history,
        
    }
    
    return render(request, 'owner/vehicle_detail.html', context)
#vehicle owners can book service
@login_required
def book_service_appointment(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user.vehicleowner)

    if request.method == 'POST':
        form = ServiceAppointmentForm(request.POST)
        if form.is_valid():
            service_request = ServiceRequest.objects.create(
                owner=request.user.vehicleowner,
                vehicle=vehicle,
                issue_description=form.cleaned_data['service_type'],
                status='pending',
                mechanic=form.cleaned_data['mechanic'],
                company=form.cleaned_data['service_center']
            )
            Appointment.objects.create(
                service_request=service_request,
                scheduled_date=form.cleaned_data['preferred_date'],
                location=form.cleaned_data['location'] or form.cleaned_data['service_center'].address,
                confirmed=False
            )
            return redirect('vehicle_detail', vehicle_id=vehicle.id)
    else:
        form = ServiceAppointmentForm()

    return render(request, 'owner/book_service_appointment.html', {'form': form, 'vehicle': vehicle})
#users can logout of their accounts
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout_confirmation')
    return render(request, 'registration/logout.html')
#The page returns a logout confirmation.
def logout_confirmation(request):
    return render(request, 'registration/logout_confirmation.html')
#Display vehicle owner dashboard
@login_required
def owner_dashboard(request):
    vehicle_owner = request.user.vehicleowner
    upcoming_appointments = vehicle_owner.service_requests.filter(status='upcoming')
    pending_service_requests = vehicle_owner.service_requests.filter(status='pending')
    
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'pending_service_requests': pending_service_requests,
        
    }
    
    return render(request, 'dashboards/owner_dashboard.html', context)



#Display mechanic dashboard
@login_required
def mechanic_dashboard(request):
    mechanic = request.user.mechanic
    
    # Count the number of assigned jobs with status 'pending' or 'in_progress'
    assigned_jobs_count = ServiceRequest.objects.filter(
        mechanic=mechanic, 
        status__in=['pending', 'in_progress']
    ).count()
    
    # Count the number of completed jobs
    completed_jobs_count = ServiceRequest.objects.filter(
        mechanic=mechanic, 
        status='completed'
    ).count()
    
    context = {
        'assigned_jobs_count': assigned_jobs_count,
        'completed_jobs_count': completed_jobs_count,
    }
    
    return render(request, 'dashboards/mechanic_dashboard.html', context)






#Display company dashboard
@login_required
def company_dashboard(request):
    # Logic specific to auto repair companies
    return render(request, 'dashboards/company_dashboard.html')

#Vehicle owner can book service
@login_required
def service_requests(request):
    # Example: Fetch service requests based on user role
    if request.user.role == 'owner':
        requests = request.user.vehicleowner.service_requests.all()
    elif request.user.role == 'mechanic':
        requests = request.user.mechanic.service_requests.all()
    elif request.user.role == 'company':
        requests = request.user.autorepaircompany.service_requests.all()
    return render(request, 'common/service_requests.html', {'requests': requests})

@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    return render(request, 'service_requests/detail.html', {'service_request': service_request})






#Mechanic can view assigned jobs
@login_required
def assigned_jobs(request):
    mechanic = request.user.mechanic
    assigned_jobs = ServiceRequest.objects.filter(mechanic=mechanic).exclude(status='completed')

    return render(request, 'mechanic/assigned_jobs.html', {
        'assigned_jobs': assigned_jobs,
    })
#Mechanic can view profile
@login_required
def profile(request):
    # Example: Mechanic profile details
    profile = request.user.mechanic
    return render(request, 'mechanic/profile.html', {'profile': profile})
#Companies can manage mechanics
@login_required
def manage_mechanics(request):
    # Example: List mechanics under a company
    mechanics = request.user.autorepaircompany.mechanic_set.all()
    return render(request, 'company/manage_mechanics.html', {'mechanics': mechanics})
#Vehicle owners can book a service
@login_required
def book_service(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.owner = request.user.vehicleowner
            service_request.status = 'pending'
            service_request.save()
            return redirect('owner_dashboard')
    else:
        form = ServiceRequestForm()

    return render(request, 'owner/book_service.html', {'form': form})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, mechanic=request.user.mechanic)

    if request.method == 'POST':
        form = ServiceRequestStatusForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('assigned_jobs')  # Redirect to the assigned jobs page after update
    else:
        form = ServiceRequestStatusForm(instance=job)

    return render(request, 'mechanic/job_detail.html', {
        'job': job,
        'form': form,
    })


@login_required
def completed_jobs(request):
    mechanic = request.user.mechanic
    completed_jobs = ServiceRequest.objects.filter(mechanic=mechanic, status='completed')

    return render(request, 'mechanic/completed_jobs.html', {
        'completed_jobs': completed_jobs,
    })    
    

@login_required
def mechanic_appointments(request):
    mechanic = request.user.mechanic
    upcoming_appointments = Appointment.objects.filter(
        service_request__mechanic=mechanic,
        scheduled_date__gte=datetime.now()
    ).order_by('scheduled_date')

    return render(request, 'mechanic/mechanic_appointments.html', {
        'upcoming_appointments': upcoming_appointments,
    })
    
    
        
@login_required
def give_feedback(request, service_request_id):
    service_request = get_object_or_404(ServiceRequest, id=service_request_id, owner=request.user.vehicleowner)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect('vehicle_detail', vehicle_id=service_request.vehicle.id)
    else:
        form = FeedbackForm(instance=service_request)

    return render(request, 'owner/give_feedback.html', {'form': form, 'service_request': service_request}) 



@login_required
def mechanic_calendar(request):
    mechanic = request.user.mechanic
    appointments = Appointment.objects.filter(service_request__mechanic=mechanic)
    
    context = {
        'appointments': appointments,
    }
    
    return render(request, 'mechanic/calendar_view.html', context)


@login_required
def mechanic_update_profile(request):
    mechanic = request.user.mechanic

    if request.method == 'POST':
        mechanic_form = MechanicProfileUpdateForm(request.POST, instance=mechanic)
        picture_form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=mechanic)

        if mechanic_form.is_valid() and picture_form.is_valid():
            mechanic_form.save()
            picture_form.save()
            return redirect('mechanic_dashboard')
    else:
        mechanic_form = MechanicProfileUpdateForm(instance=mechanic)
        picture_form = ProfilePictureUpdateForm(instance=mechanic)

    return render(request, 'mechanic/update_profile.html', {
        'mechanic_form': mechanic_form,
        'picture_form': picture_form,
    })
 
 
 
@login_required    
def search_mechanics(request):
    form = MechanicSearchForm(request.GET or None)
    mechanics = Mechanic.objects.all()

    if form.is_valid():
        if form.cleaned_data['city']:
            mechanics = mechanics.filter(city__icontains=form.cleaned_data['city'])
        if form.cleaned_data['state']:
            mechanics = mechanics.filter(state__icontains=form.cleaned_data['state'])

    context = {
        'form': form,
        'mechanics': mechanics,
    }
    return render(request, 'owner/search_mechanics.html', context)








# views.py

from rest_framework import generics
from .models import CustomUser, VehicleOwner, Vehicle, Mechanic, AutoRepairCompany, ServiceRequest, Appointment
from .serializers import CustomUserSerializer, VehicleOwnerSerializer, VehicleSerializer, MechanicSerializer, AutoRepairCompanySerializer, ServiceRequestSerializer, AppointmentSerializer

# User Views
class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

# VehicleOwner Views
class VehicleOwnerList(generics.ListCreateAPIView):
    queryset = VehicleOwner.objects.all()
    serializer_class = VehicleOwnerSerializer

class VehicleOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleOwner.objects.all()
    serializer_class = VehicleOwnerSerializer

# Vehicle Views
class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Mechanic Views
class MechanicList(generics.ListCreateAPIView):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

class MechanicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

# AutoRepairCompany Views
class AutoRepairCompanyList(generics.ListCreateAPIView):
    queryset = AutoRepairCompany.objects.all()
    serializer_class = AutoRepairCompanySerializer

class AutoRepairCompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AutoRepairCompany.objects.all()
    serializer_class = AutoRepairCompanySerializer

# ServiceRequest Views
class ServiceRequestList(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

# Appointment Views
class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    