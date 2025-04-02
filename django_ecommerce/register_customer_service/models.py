from django.contrib.auth.models import AbstractUser
from django.db import models

class RegisteredCustomer(AbstractUser):
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    loyalty_points = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'register_customer'

class RegisteredAddress(models.Model):
    customer = models.ForeignKey(RegisteredCustomer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'register_customer'

class EmailVerification(models.Model):
    customer = models.OneToOneField(RegisteredCustomer, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        app_label = 'register_customer'
