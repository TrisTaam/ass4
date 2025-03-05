from django.db import models

class Shipping(models.Model):
    order_id = models.IntegerField()  # Changed from ForeignKey to IntegerField    shipping_method = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_number = models.CharField(max_length=100, blank=True)

    class Meta:
        app_label = 'shipping'