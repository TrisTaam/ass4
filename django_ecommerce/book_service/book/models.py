from django.db import models

class Book(models.Model):
    """
    Book model representing items in the book service
    """
    BINDING_CHOICES = [
        ('HC', 'Hardcover'),
        ('PB', 'Paperback'),
        ('EB', 'E-Book'),
        ('AB', 'Audiobook'),
    ]
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    binding = models.CharField(max_length=2, choices=BINDING_CHOICES)
    page_count = models.IntegerField()
    language = models.CharField(max_length=100, default='English')
    genre = models.CharField(max_length=100)
    description = models.TextField()
    
    # Common item fields
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    class Meta:
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['author']),
            models.Index(fields=['genre']),
        ] 