from djongo import models

class Item(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)  # book, mobile, clothes, shoes
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.URLField()
    specific_data = models.JSONField()  # e.g., {"author": "X"} for books

    class Meta:
        app_label = 'items'