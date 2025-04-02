from django.contrib import admin
from .models import Clothes

@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'gender', 'category', 'material', 'primary_color', 'price', 'discount_percentage', 'is_available')
    list_filter = ('gender', 'category', 'material', 'primary_color', 'size_system', 'is_available')
    search_fields = ('name', 'brand', 'sku', 'material', 'description')
    readonly_fields = ('created_at', 'updated_at') 