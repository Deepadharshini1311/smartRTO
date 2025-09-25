# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, VehicleForm, LicenseForm, ApplicationForm
from .models import Application, Vehicle, License
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'rtoapp/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'rtoapp/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'rtoapp/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    apps = Application.objects.filter(user=request.user).order_by('-submission_date')
    licenses = License.objects.filter(user=request.user)
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'rtoapp/dashboard.html', {'apps':apps, 'licenses':licenses, 'vehicles':vehicles})

@login_required
def apply_license(request):
    if request.method == 'POST':
        lform = LicenseForm(request.POST)
        appform = ApplicationForm(request.POST, request.FILES)
        if lform.is_valid() and appform.is_valid():
            license_obj = lform.save(commit=False)
            license_obj.user = request.user
            license_obj.status = 'Pending'
            license_obj.save()
            app = appform.save(commit=False)
            app.user = request.user
            app.app_type = 'License'
            app.related_license = license_obj
            app.save()
            return redirect('dashboard')
    else:
        lform = LicenseForm()
        appform = ApplicationForm()
    return render(request, 'rtoapp/apply_license.html', {'lform': lform, 'appform': appform})

@login_required
def apply_vehicle(request):
    if request.method == 'POST':
        vform = VehicleForm(request.POST)
        appform = ApplicationForm(request.POST, request.FILES)
        if vform.is_valid() and appform.is_valid():
            vehicle = vform.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            app = appform.save(commit=False)
            app.user = request.user
            app.app_type = 'Vehicle'
            app.related_vehicle = vehicle
            app.save()
            return redirect('dashboard')
    else:
        vform = VehicleForm()
        appform = ApplicationForm()
    return render(request, 'rtoapp/apply_vehicle.html', {'vform': vform, 'appform': appform})

# Simple check: treat staff (is_staff) users as RTO officers
def is_officer(user):
    return user.is_staff

@user_passes_test(is_officer)
def officer_dashboard(request):
    pending_apps = Application.objects.filter(status='Pending').order_by('submission_date')
    return render(request, 'rtoapp/officer_dashboard.html', {'pending_apps': pending_apps})

@user_passes_test(is_officer)
def approve_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    app.status = 'Approved'
    app.save()

    # If license application -> set license fields and generate QR
    if app.app_type == 'License' and app.related_license:
        lic = app.related_license
        lic.status = 'Approved'
        lic.issue_date = date.today()
        lic.expiry_date = date.today() + timedelta(days=365*5)  # 5 years
        # generate QR
        qr_data = f"LIC:{lic.id};USER:{lic.user.username};ISSUE:{lic.issue_date}"
        img = qrcode.make(qr_data)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filebuffer = ContentFile(buffer.getvalue())
        lic.qr_image.save(f'license_qr_{lic.id}.png', filebuffer)
        lic.save()

    # If vehicle app - you can similarly update vehicle/RC
    return redirect('officer_dashboard')

@user_passes_test(is_officer)
def reject_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    app.status = 'Rejected'
    app.save()
    return redirect('officer_dashboard')
