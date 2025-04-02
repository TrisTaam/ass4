#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vip_customer_service.settings')
django.setup()

from vip_customer_service.models import VIPBenefit

def create_initial_benefits():
    """Create initial VIP benefits for different tiers"""
    
    # Clear existing benefits if needed
    # VIPBenefit.objects.all().delete()
    
    # Define benefits for different tiers
    benefits = [
        # Bronze benefits
        {
            'name': 'Standard Shipping Discount',
            'description': 'Free standard shipping on all orders',
            'benefit_type': 'free_shipping',
            'eligible_tiers': 'bronze,silver,gold,platinum',
        },
        {
            'name': 'Basic Discount',
            'description': '5% discount on all purchases',
            'benefit_type': 'discount',
            'discount_percent': 5,
            'eligible_tiers': 'bronze,silver,gold,platinum',
        },
        
        # Silver benefits
        {
            'name': 'Express Shipping',
            'description': 'Free express shipping on orders over $50',
            'benefit_type': 'free_shipping',
            'eligible_tiers': 'silver,gold,platinum',
        },
        {
            'name': 'Silver Discount',
            'description': '10% discount on all purchases',
            'benefit_type': 'discount',
            'discount_percent': 10,
            'eligible_tiers': 'silver,gold,platinum',
        },
        {
            'name': 'Early Sale Access',
            'description': 'Access to sales 24 hours before regular customers',
            'benefit_type': 'early_access',
            'eligible_tiers': 'silver,gold,platinum',
        },
        
        # Gold benefits
        {
            'name': 'Priority Shipping',
            'description': 'Free priority shipping on all orders',
            'benefit_type': 'free_shipping',
            'eligible_tiers': 'gold,platinum',
        },
        {
            'name': 'Gold Discount',
            'description': '15% discount on all purchases',
            'benefit_type': 'discount',
            'discount_percent': 15,
            'eligible_tiers': 'gold,platinum',
        },
        {
            'name': 'Quarterly Gift',
            'description': 'Receive a free gift every quarter',
            'benefit_type': 'gift',
            'eligible_tiers': 'gold,platinum',
        },
        {
            'name': 'Exclusive Products',
            'description': 'Access to exclusive gold-tier products',
            'benefit_type': 'exclusive',
            'eligible_tiers': 'gold,platinum',
        },
        
        # Platinum benefits
        {
            'name': 'International Shipping',
            'description': 'Free international shipping on all orders',
            'benefit_type': 'free_shipping',
            'eligible_tiers': 'platinum',
        },
        {
            'name': 'Platinum Discount',
            'description': '20% discount on all purchases',
            'benefit_type': 'discount',
            'discount_percent': 20,
            'eligible_tiers': 'platinum',
        },
        {
            'name': 'Monthly Gift',
            'description': 'Receive a free gift every month',
            'benefit_type': 'gift',
            'eligible_tiers': 'platinum',
        },
        {
            'name': 'Premium Exclusive Products',
            'description': 'Access to premium exclusive platinum-tier products',
            'benefit_type': 'exclusive',
            'eligible_tiers': 'platinum',
        },
        {
            'name': 'VIP Events',
            'description': 'Invitations to exclusive VIP events and product launches',
            'benefit_type': 'event',
            'eligible_tiers': 'platinum',
        },
        {
            'name': 'Dedicated Support',
            'description': 'Access to a dedicated customer support representative',
            'benefit_type': 'exclusive',
            'eligible_tiers': 'platinum',
        },
    ]
    
    # Create benefits
    for benefit_data in benefits:
        benefit, created = VIPBenefit.objects.get_or_create(
            name=benefit_data['name'],
            defaults={
                'description': benefit_data['description'],
                'benefit_type': benefit_data['benefit_type'],
                'discount_percent': benefit_data.get('discount_percent', 0),
                'eligible_tiers': benefit_data['eligible_tiers'],
            }
        )
        
        if created:
            print(f"Created benefit: {benefit.name}")
        else:
            print(f"Benefit already exists: {benefit.name}")

if __name__ == '__main__':
    print("Creating initial VIP benefits...")
    create_initial_benefits()
    print("Done!") 