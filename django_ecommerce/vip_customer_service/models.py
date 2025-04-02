from django.contrib.auth.models import AbstractUser
from django.db import models

class VIPCustomer(AbstractUser):
    VIP_TIERS = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )
    
    vip_tier = models.CharField(max_length=10, choices=VIP_TIERS, default='bronze')
    loyalty_points = models.IntegerField(default=1000)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    membership_date = models.DateTimeField(auto_now_add=True)
    membership_expiry = models.DateTimeField(null=True, blank=True)
    annual_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        app_label = 'vip_customer'

class VIPAddress(models.Model):
    customer = models.ForeignKey(VIPCustomer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'vip_customer'

class VIPBenefit(models.Model):
    BENEFIT_TYPES = (
        ('discount', 'Discount'),
        ('free_shipping', 'Free Shipping'),
        ('gift', 'Free Gift'),
        ('early_access', 'Early Access'),
        ('exclusive', 'Exclusive Product Access'),
        ('event', 'Special Event Invite'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    benefit_type = models.CharField(max_length=20, choices=BENEFIT_TYPES)
    discount_percent = models.IntegerField(default=0, help_text="Only applicable for discount benefits")
    eligible_tiers = models.CharField(max_length=100, help_text="Comma-separated list of eligible VIP tiers")
    
    class Meta:
        app_label = 'vip_customer'

class VIPCustomerBenefit(models.Model):
    customer = models.ForeignKey(VIPCustomer, on_delete=models.CASCADE, related_name='benefits')
    benefit = models.ForeignKey(VIPBenefit, on_delete=models.CASCADE)
    activated_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'vip_customer'
        unique_together = ('customer', 'benefit')
