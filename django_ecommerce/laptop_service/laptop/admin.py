from django.contrib import admin
from .models import Laptop

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'processor_brand', 'ram', 'storage_capacity', 'price', 'stock_quantity', 'is_available')
    list_filter = ('brand', 'processor_brand', 'ram', 'storage_type', 'is_available')
    search_fields = ('name', 'brand', 'model_number', 'processor_model')
    readonly_fields = ('created_at', 'updated_at') 