from djongo import models

class Item(models.Model):
    """
    For reference only - this model is not used for data storage.
    In the pure router architecture, data is only stored in specialized services:
    - Book Service
    - Laptop Service
    - Mobile Service
    - Clothes Service
    
    This model exists only to define the expected structure for documentation purposes.
    """
    ITEM_TYPES = [
        ('generic', 'Generic Item'),
        ('book', 'Book'),
        ('laptop', 'Laptop'),
        ('mobile', 'Mobile Device'),
        ('clothes', 'Clothes'),
    ]
    
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=ITEM_TYPES, default='generic')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.URLField()
    specific_data = models.JSONField()  # e.g., {"author": "X"} for books

    class Meta:
        app_label = 'items'
        
    def __str__(self):
        return f"{self.name} ({self.type})"