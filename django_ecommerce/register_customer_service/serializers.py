from rest_framework import serializers
from .models import RegisteredCustomer, RegisteredAddress, EmailVerification

class RegisteredAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredAddress
        fields = ['id', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']

class RegisteredCustomerSerializer(serializers.ModelSerializer):
    addresses = RegisteredAddressSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = RegisteredCustomer
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'email_verified', 
                  'phone_number', 'date_of_birth', 'registration_date', 'loyalty_points', 
                  'addresses', 'password']
        read_only_fields = ['email_verified', 'registration_date', 'loyalty_points']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = RegisteredCustomer(**validated_data)
        user.set_password(password)
        user.save()
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['id', 'customer', 'token', 'created_at', 'expires_at']
        read_only_fields = ['created_at']
