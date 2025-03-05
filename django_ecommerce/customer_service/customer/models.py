from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    CUSTOMER_TYPES = (
        ('guest', 'Guest'),
        ('new', 'New'),
        ('regular', 'Regular'),
        ('vip', 'VIP'),
    )
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, default='new')
    loyalty_points = models.IntegerField(default=0)

    class Meta:
        app_label = 'customer'

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    class Meta:
        app_label = 'customer'