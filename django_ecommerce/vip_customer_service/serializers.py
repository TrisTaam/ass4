from rest_framework import serializers
from .models import VIPCustomer, VIPAddress, VIPBenefit, VIPCustomerBenefit

class VIPAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIPAddress
        fields = ['id', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']

class VIPBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIPBenefit
        fields = ['id', 'name', 'description', 'benefit_type', 'discount_percent', 'eligible_tiers']

class VIPCustomerBenefitSerializer(serializers.ModelSerializer):
    benefit = VIPBenefitSerializer(read_only=True)
    
    class Meta:
        model = VIPCustomerBenefit
        fields = ['id', 'benefit', 'activated_date', 'expiry_date', 'is_active', 'usage_count']

class VIPCustomerSerializer(serializers.ModelSerializer):
    addresses = VIPAddressSerializer(many=True, read_only=True)
    benefits = VIPCustomerBenefitSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = VIPCustomer
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'vip_tier',
                 'loyalty_points', 'phone_number', 'date_of_birth', 'membership_date',
                 'membership_expiry', 'annual_spend', 'addresses', 'benefits', 'password']
        read_only_fields = ['membership_date', 'loyalty_points', 'annual_spend']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = VIPCustomer(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
