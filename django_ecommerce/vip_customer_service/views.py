from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import timedelta
import uuid

from .forms import VIPCustomerForm, VIPAddressForm, VIPTierUpgradeForm
from .models import VIPCustomer, VIPAddress, VIPBenefit, VIPCustomerBenefit
from .serializers import (VIPCustomerSerializer, VIPAddressSerializer, 
                          VIPBenefitSerializer, VIPCustomerBenefitSerializer)

# Create your views here.

# Web views
def home_view(request):
    """Home page for VIP service"""
    benefits = VIPBenefit.objects.all()
    return render(request, 'home.html', {'benefits': benefits})

def register_view(request):
    """Handles VIP registration"""
    if request.method == 'POST':
        form = VIPCustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to our VIP program! You've been registered successfully.")
            return redirect('vip_dashboard')
    else:
        form = VIPCustomerForm()
    return render(request, 'register.html', {'form': form})

@login_required
def vip_dashboard(request):
    """Dashboard for VIP customers"""
    customer = request.user
    addresses = VIPAddress.objects.filter(customer=customer)
    active_benefits = VIPCustomerBenefit.objects.filter(
        customer=customer, 
        is_active=True
    ).select_related('benefit')
    
    # Get eligible benefits that user doesn't have yet
    user_tier = customer.vip_tier
    current_benefit_ids = active_benefits.values_list('benefit_id', flat=True)
    
    eligible_benefits = VIPBenefit.objects.exclude(id__in=current_benefit_ids)
    new_eligible_benefits = []
    
    for benefit in eligible_benefits:
        tiers = benefit.eligible_tiers.split(',')
        if user_tier in tiers:
            new_eligible_benefits.append(benefit)
    
    context = {
        'customer': customer,
        'addresses': addresses,
        'active_benefits': active_benefits,
        'eligible_benefits': new_eligible_benefits
    }
    
    return render(request, 'vip_dashboard.html', context)

@login_required
def add_address_view(request):
    """Add a new address for VIP customer"""
    if request.method == 'POST':
        form = VIPAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            
            # If this is set as default, unset any existing default
            if address.is_default:
                VIPAddress.objects.filter(
                    customer=request.user, 
                    is_default=True
                ).update(is_default=False)
                
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('vip_dashboard')
    else:
        form = VIPAddressForm()
    return render(request, 'add_address.html', {'form': form})

@login_required
def upgrade_tier_view(request):
    """Upgrade VIP tier"""
    if request.method == 'POST':
        form = VIPTierUpgradeForm(request.POST, user=request.user)
        if form.is_valid():
            previous_tier = request.user.vip_tier
            request.user.vip_tier = form.cleaned_data['vip_tier']
            request.user.save()
            
            # Add tier-appropriate benefits
            new_tier = request.user.vip_tier
            add_tier_benefits(request.user, new_tier)
            
            messages.success(request, f"Congratulations! You've been upgraded from {previous_tier.capitalize()} to {new_tier.capitalize()}!")
            return redirect('vip_dashboard')
    else:
        form = VIPTierUpgradeForm(user=request.user)
    return render(request, 'upgrade_tier.html', {'form': form})

@login_required
def activate_benefit_view(request, benefit_id):
    """Activate a new benefit for the VIP customer"""
    benefit = get_object_or_404(VIPBenefit, id=benefit_id)
    
    # Check if user is eligible for this benefit
    eligible_tiers = benefit.eligible_tiers.split(',')
    if request.user.vip_tier not in eligible_tiers:
        messages.error(request, f"You need to be a {', '.join(t.capitalize() for t in eligible_tiers)} member to activate this benefit.")
        return redirect('vip_dashboard')
    
    # Check if already has this benefit
    existing_benefit = VIPCustomerBenefit.objects.filter(
        customer=request.user,
        benefit=benefit
    ).first()
    
    if existing_benefit:
        if not existing_benefit.is_active:
            existing_benefit.is_active = True
            existing_benefit.save()
            messages.success(request, f"The '{benefit.name}' benefit has been reactivated!")
        else:
            messages.info(request, f"You already have the '{benefit.name}' benefit active.")
    else:
        # Create a new benefit
        VIPCustomerBenefit.objects.create(
            customer=request.user,
            benefit=benefit,
            is_active=True
        )
        messages.success(request, f"The '{benefit.name}' benefit has been added to your account!")
    
    return redirect('vip_dashboard')

# Helper function to add tier benefits
def add_tier_benefits(user, tier):
    """Add all benefits appropriate for a given tier"""
    eligible_benefits = VIPBenefit.objects.all()
    for benefit in eligible_benefits:
        tiers = benefit.eligible_tiers.split(',')
        if tier in tiers:
            # Add this benefit if user doesn't have it already
            VIPCustomerBenefit.objects.get_or_create(
                customer=user,
                benefit=benefit,
                defaults={'is_active': True}
            )

# API ViewSets
class VIPCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = VIPCustomerSerializer
    
    def get_queryset(self):
        # Admin sees all, customers see only themselves
        if self.request.user.is_staff:
            return VIPCustomer.objects.all()
        return VIPCustomer.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get the current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upgrade_tier(self, request, pk=None):
        """Upgrade a VIP customer's tier"""
        customer = self.get_object()
        new_tier = request.data.get('vip_tier')
        
        # Validate tier
        if new_tier not in dict(VIPCustomer.VIP_TIERS):
            return Response(
                {"error": f"Invalid tier. Choose from {list(dict(VIPCustomer.VIP_TIERS).keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check tier order
        tier_order = ['bronze', 'silver', 'gold', 'platinum']
        current_index = tier_order.index(customer.vip_tier)
        new_index = tier_order.index(new_tier)
        
        if new_index <= current_index:
            return Response(
                {"error": f"Cannot downgrade from {customer.vip_tier} to {new_tier}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update tier and add benefits
        customer.vip_tier = new_tier
        customer.save()
        add_tier_benefits(customer, new_tier)
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

class VIPAddressViewSet(viewsets.ModelViewSet):
    serializer_class = VIPAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return VIPAddress.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        # If new address is default, unset existing defaults
        if serializer.validated_data.get('is_default', False):
            VIPAddress.objects.filter(
                customer=self.request.user, 
                is_default=True
            ).update(is_default=False)
            
        serializer.save(customer=self.request.user)

class VIPBenefitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VIPBenefitSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = VIPBenefit.objects.all()
        
        # Filter by tier if requested
        tier = self.request.query_params.get('tier')
        if tier:
            filtered = []
            for benefit in queryset:
                eligible_tiers = benefit.eligible_tiers.split(',')
                if tier in eligible_tiers:
                    filtered.append(benefit.id)
            queryset = queryset.filter(id__in=filtered)
            
        return queryset

class VIPCustomerBenefitViewSet(viewsets.ModelViewSet):
    serializer_class = VIPCustomerBenefitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return VIPCustomerBenefit.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        benefit = serializer.validated_data.get('benefit')
        
        # Validate eligibility
        eligible_tiers = benefit.eligible_tiers.split(',')
        if self.request.user.vip_tier not in eligible_tiers:
            raise serializers.ValidationError(
                f"You need to be a {', '.join(eligible_tiers)} member to activate this benefit."
            )
        
        serializer.save(customer=self.request.user)
