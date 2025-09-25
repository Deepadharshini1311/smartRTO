from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Vehicle, License

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['chassis_no','engine_no','vehicle_type','insurance_details']

class LicenseForm(forms.ModelForm):
    LICENSE_TYPE_CHOICES = [
        ('Learner', 'Learner'),
        ('Permanent', 'Permanent'),
        ('LMV', 'Light Motor Vehicle'),
        ('HMV', 'Heavy Motor Vehicle'),
        ('Motorcycle', 'Motorcycle'),
        ('Transport', 'Transport Vehicle'),
    ]
    license_type = forms.ChoiceField(choices=LICENSE_TYPE_CHOICES)
    class Meta:
        model = License
        fields = ['license_type']

class ApplicationForm(forms.ModelForm):
    APP_TYPE_CHOICES = [
        ('New License', 'New License Application'),
        ('Renewal', 'Renewal'),
        ('Duplicate', 'Duplicate License'),
        ('Change Address', 'Change of Address'),
        ('International', 'International Driving Permit'),
    ]
    app_type = forms.ChoiceField(choices=APP_TYPE_CHOICES)
    class Meta:
        model = Application
        fields = ['app_type','document']
