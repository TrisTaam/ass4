from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import timedelta
import uuid

from .forms import CustomerRegistrationForm, AddressForm
from .models import RegisteredCustomer, RegisteredAddress, EmailVerification
from .serializers import RegisteredCustomerSerializer, RegisteredAddressSerializer, EmailVerificationSerializer

# Create your views here.

# Web views
def register_view(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create email verification token
            token = str(uuid.uuid4())
            expires = timezone.now() + timedelta(days=2)
            EmailVerification.objects.create(
                customer=user,
                token=token,
                expires_at=expires
            )
            
            # TODO: Send verification email
            
            login(request, user)
            return redirect('profile')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    addresses = RegisteredAddress.objects.filter(customer=request.user)
    return render(request, 'profile.html', {'user': request.user, 'addresses': addresses})

@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user
            
            # If this is set as default, unset any existing default
            if address.is_default:
                RegisteredAddress.objects.filter(
                    customer=request.user, 
                    is_default=True
                ).update(is_default=False)
                
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        
        # Check if token is expired
        if verification.expires_at < timezone.now():
            return render(request, 'verification_failed.html', {'reason': 'Token expired'})
        
        # Mark email as verified
        customer = verification.customer
        customer.email_verified = True
        customer.save()
        
        # Delete the verification token
        verification.delete()
        
        return render(request, 'verification_success.html')
    except EmailVerification.DoesNotExist:
        return render(request, 'verification_failed.html', {'reason': 'Invalid token'})

# API ViewSets
class RegisteredCustomerViewSet(viewsets.ModelViewSet):
    queryset = RegisteredCustomer.objects.all()
    serializer_class = RegisteredCustomerSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create email verification token
            token = str(uuid.uuid4())
            expires = timezone.now() + timedelta(days=2)
            EmailVerification.objects.create(
                customer=user,
                token=token,
                expires_at=expires
            )
            
            # TODO: Send verification email
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class RegisteredAddressViewSet(viewsets.ModelViewSet):
    serializer_class = RegisteredAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return RegisteredAddress.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        # If this is set as default, unset any existing default
        if serializer.validated_data.get('is_default', False):
            RegisteredAddress.objects.filter(
                customer=self.request.user, 
                is_default=True
            ).update(is_default=False)
            
        serializer.save(customer=self.request.user)
