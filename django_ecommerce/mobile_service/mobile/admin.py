from django.contrib import admin
from .models import Mobile

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'ram', 'storage', 'network_type', 'screen_size', 'price', 'stock_quantity', 'is_available')
    list_filter = ('brand', 'network_type', 'ram', 'operating_system', 'is_available')
    search_fields = ('name', 'brand', 'model_number', 'processor')
    readonly_fields = ('created_at', 'updated_at') 