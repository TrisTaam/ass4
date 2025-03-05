from django.db import models

class Cart(models.Model):
    customer_id = models.IntegerField()  # Reference to Customer
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_id = models.CharField(max_length=24)  # MongoDB ObjectId
    quantity = models.IntegerField()
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'cart'