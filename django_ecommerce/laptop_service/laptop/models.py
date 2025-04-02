from djongo import models

class Laptop(models.Model):
    PROCESSOR_BRANDS = [
        ('intel', 'Intel'),
        ('amd', 'AMD'),
        ('arm', 'ARM'),
        ('apple', 'Apple'),
        ('other', 'Other'),
    ]
    
    STORAGE_TYPES = [
        ('ssd', 'SSD'),
        ('hdd', 'HDD'),
        ('hybrid', 'Hybrid'),
    ]
    
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    
    # Processor details
    processor_brand = models.CharField(max_length=50, choices=PROCESSOR_BRANDS)
    processor_model = models.CharField(max_length=100)
    processor_speed = models.DecimalField(max_digits=4, decimal_places=2)  # GHz
    processor_cores = models.IntegerField()
    
    # Memory
    ram = models.IntegerField()  # GB
    
    # Storage
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPES)
    storage_capacity = models.IntegerField()  # GB
    
    # Display
    screen_size = models.DecimalField(max_digits=4, decimal_places=1)  # inches
    resolution = models.CharField(max_length=50)  # e.g., 1920x1080
    is_touchscreen = models.BooleanField(default=False)
    
    # Graphics
    graphics_card = models.CharField(max_length=100)
    graphics_memory = models.IntegerField(null=True, blank=True)  # GB
    
    # Connectivity
    has_wifi = models.BooleanField(default=True)
    has_bluetooth = models.BooleanField(default=True)
    ports = models.JSONField()  # e.g., {"usb_a": 2, "usb_c": 1, "hdmi": 1}
    
    # Battery
    battery_capacity = models.IntegerField()  # mAh
    battery_life = models.DecimalField(max_digits=4, decimal_places=1)  # hours
    
    # Physical
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # kg
    dimensions = models.CharField(max_length=100)  # e.g., "30.41 x 21.24 x 1.8 cm"
    
    # Business details
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.URLField()
    is_available = models.BooleanField(default=True)
    
    # OS
    operating_system = models.CharField(max_length=100)
    
    # Other
    warranty_period = models.IntegerField()  # months
    color = models.CharField(max_length=50)
    description = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'laptop'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['brand']),
            models.Index(fields=['price']),
            models.Index(fields=['processor_brand']),
            models.Index(fields=['ram']),
            models.Index(fields=['storage_capacity']),
        ]
    
    def __str__(self):
        return f"{self.brand} {self.name} ({self.processor_brand} {self.processor_model}, {self.ram}GB RAM, {self.storage_capacity}GB {self.storage_type})" 