from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import VehicleOwner, Vehicle,Appointment, ServiceRequest,Mechanic, AutoRepairCompany

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']
        
    def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user    


class VehicleOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = VehicleOwner
        fields = ['profile_picture', 'phone_number', 'address']
        
       
       
        
class VehicleOwnerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = VehicleOwner
        fields = ['profile_picture', 'phone_number', 'address']
        widgets = {
            'profile_picture': forms.FileInput(),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
        }
        
        
                

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'year', 'vin']
        
        
class ServiceAppointmentForm(forms.ModelForm):
    service_type = forms.CharField(max_length=100, label="Service Type", help_text="E.g., Oil Change, Brake Repair")
    preferred_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label="Preferred Date")
    preferred_time = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Preferred Time")
    location = forms.CharField(max_length=255, label="Location", required=False)
    
    mechanic = forms.ModelChoiceField(queryset=Mechanic.objects.all(), required=False, label="Preferred Mechanic")
    service_center = forms.ModelChoiceField(queryset=AutoRepairCompany.objects.all(), required=False, label="Preferred Service Center")
    
    class Meta:
        model = Appointment
        fields = ['preferred_date', 'preferred_time', 'location', 'mechanic', 'service_center']    


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['vehicle', 'issue_description', 'mechanic', 'company']     
        
        
class ServiceRequestStatusForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status']        
        
        
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['feedback','rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Leave your feedback here...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }        
        
        
        

class MechanicProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['phone_number', 'specialty', 'experience_years']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        
class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['profile_picture']        
        
        
class MechanicSearchForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)