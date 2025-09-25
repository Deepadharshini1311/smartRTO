# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

APPLICATION_STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chassis_no = models.CharField(max_length=50)
    engine_no = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=30)
    insurance_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} - {self.chassis_no}"

class License(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_type = models.CharField(max_length=20)  # Learner / Permanent
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Pending')
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_type} - {self.status}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_type = models.CharField(max_length=30)  # License / Vehicle
    related_license = models.ForeignKey(License, null=True, blank=True, on_delete=models.SET_NULL)
    related_vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Pending')
    document = models.FileField(upload_to='documents/', blank=True, null=True)  # e.g. ID proof

    def __str__(self):
        return f"{self.user.username} - {self.app_type} - {self.status}"

