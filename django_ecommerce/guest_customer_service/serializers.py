from rest_framework import serializers
from .models import GuestCustomer, GuestAddress

class GuestAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestAddress
        fields = ['id', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']

class GuestCustomerSerializer(serializers.ModelSerializer):
    addresses = GuestAddressSerializer(many=True, read_only=True)
    
    class Meta:
        model = GuestCustomer
        fields = ['id', 'session_id', 'created_at', 'last_activity', 'addresses'] 