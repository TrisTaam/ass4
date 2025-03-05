from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['_id', 'name', 'category', 'description', 'price', 'stock_quantity', 'image_url', 'specific_data']