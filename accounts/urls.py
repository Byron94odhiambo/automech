from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import setup_profile
from .views import add_vehicle, search_mechanics, delete_vehicle,owner_dashboard, mechanic_dashboard, company_dashboard,edit_vehicle, vehicle_detail,book_service_appointment,update_profile,mechanic_appointments,mechanic_calendar
from .views import CustomUserList, CustomUserDetail, VehicleOwnerList, VehicleOwnerDetail, VehicleList, VehicleDetail, MechanicList, MechanicDetail, AutoRepairCompanyList, AutoRepairCompanyDetail, ServiceRequestList, ServiceRequestDetail, AppointmentList, AppointmentDetail
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    
    #General Functionality
    path('logout/', views.custom_logout, name='logout'),
    path('logout/confirmation/', views.logout_confirmation, name='logout_confirmation'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('setup-profile/', setup_profile, name='setup_profile'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
   
    
   
    
    #Vehicle urls
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('owner/vehicle/<int:vehicle_id>/', vehicle_detail, name='vehicle_detail'),
    path('owner/add-vehicle/', add_vehicle, name='add_vehicle'),
    path('owner/vehicle/edit/<int:vehicle_id>/', edit_vehicle, name='edit_vehicle'),
    path('owner/vehicle/<int:vehicle_id>/book-appointment/', book_service_appointment, name='book_service_appointment'),
    path('owner/update-profile/', update_profile, name='update_profile'),
    path('owner/update-password/', auth_views.PasswordChangeView.as_view(template_name='owner/update_password.html'), name='password_change'),
    path('owner/update-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='owner/password_change_done.html'), name='password_change_done'),
    path('service-requests/', views.service_requests, name='service_requests'),
    path('service-request/<int:service_request_id>/give-feedback/', views.give_feedback, name='give_feedback'),
    path('service-requests/<int:pk>/', views.service_request_detail, name='service_request_detail'),
    path('search-mechanics/', search_mechanics, name='search_mechanics'),
     path('owner/vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    
    
    #Mechanic functionality
    path('mechanic/dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('assigned-jobs/', views.assigned_jobs, name='assigned_jobs'),
    path('assigned-jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('profile/', views.profile, name='profile'),
    path('mechanic/completed-jobs/', views.completed_jobs, name='completed_jobs'),
    path('mechanic/appointments/', views.mechanic_appointments, name='mechanic_appointments'),
    path('mechanic/calendar/', views.mechanic_calendar, name='mechanic_calendar'),
    path('mechanic/update-profile/', views.mechanic_update_profile, name='mechanic_update_profile'),
    path('mechanic/update-password/', auth_views.PasswordChangeView.as_view(template_name='mechanic/password_change.html'), name='password_change'),
    path('mechanic/update-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='mechanic/password_change_done.html'), name='password_change_done'),
    
    
    
    #Company functionality
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('manage-mechanics/', views.manage_mechanics, name='manage_mechanics'),
    
    
    
    
    
    
    
    
    
    #API endpoints
    path('users/', CustomUserList.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetail.as_view(), name='user-detail'),
    path('vehicle-owners/', VehicleOwnerList.as_view(), name='vehicle-owner-list'),
    path('vehicle-owners/<int:pk>/', VehicleOwnerDetail.as_view(), name='vehicle-owner-detail'),
    path('vehicles/', VehicleList.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('mechanics/', MechanicList.as_view(), name='mechanic-list'),
    path('mechanics/<int:pk>/', MechanicDetail.as_view(), name='mechanic-detail'),
    path('companies/', AutoRepairCompanyList.as_view(), name='company-list'),
    path('companies/<int:pk>/', AutoRepairCompanyDetail.as_view(), name='company-detail'),
    path('service-requests/', ServiceRequestList.as_view(), name='service-request-list'),
    path('service-requests/<int:pk>/', ServiceRequestDetail.as_view(), name='service-request-detail'),
    path('appointments/', AppointmentList.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetail.as_view(), name='appointment-detail'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)