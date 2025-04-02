from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .forms import CustomerRegistrationForm
from .models import Customer, Address
from .serializers import CustomerSerializer
import requests
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Service URLs
GUEST_SERVICE_URL = "http://guest-customer:8001/api"
REGISTERED_SERVICE_URL = "http://register-customer:8007/api"
VIP_SERVICE_URL = "http://vip-customer:8008/api"

# Traditional view (keep for web interface)
def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'profile.html', {'user': request.user})

from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Perform the login action
            from django.contrib.auth import login
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Redirect to the profile page after successful login
    return render(request, 'login.html', {'form': form})

# Customer service routing functions
@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, customer_id):
    """
    Route customer detail requests to the appropriate service based on customer type
    """
    # Check customer type (this would normally come from authentication/database)
    customer_type = _determine_customer_type(request, customer_id)
    
    # Route to appropriate service
    if customer_type == 'vip':
        return _route_to_vip_service(request, customer_id)
    elif customer_type == 'registered':
        return _route_to_registered_service(request, customer_id)
    else:  # default to guest
        return _route_to_guest_service(request, customer_id)

@api_view(['GET', 'POST'])
def customer_list(request):
    """
    Route customer list requests to the appropriate service based on authentication
    """
    # If user is authenticated, determine customer type
    if request.user.is_authenticated:
        customer_type = _determine_customer_type(request)
        
        if customer_type == 'vip':
            return _route_to_vip_service_list(request)
        elif customer_type == 'registered':
            return _route_to_registered_service_list(request)
    
    # Default to guest service for unauthenticated users or if type can't be determined
    return _route_to_guest_service_list(request)

@api_view(['GET', 'PUT', 'DELETE'])
def guest_customer_detail(request, customer_id):
    """Direct proxy to guest customer service"""
    return _route_to_guest_service(request, customer_id)

@api_view(['GET', 'PUT', 'DELETE'])
def registered_customer_detail(request, customer_id):
    """Direct proxy to registered customer service"""
    return _route_to_registered_service(request, customer_id)

@api_view(['GET', 'PUT', 'DELETE'])
def vip_customer_detail(request, customer_id):
    """Direct proxy to VIP customer service"""
    return _route_to_vip_service(request, customer_id)

# Helper functions for routing
def _determine_customer_type(request, customer_id=None):
    """
    Determine the customer type based on user authentication and database lookup
    """
    # Check headers first (useful for API gateway forwarding)
    customer_type = request.META.get('HTTP_X_CUSTOMER_TYPE', '')
    if customer_type in ['vip', 'registered', 'guest']:
        return customer_type
    
    # If no header, check if user is authenticated and look up in DB
    if request.user.is_authenticated:
        try:
            # This assumes Customer model has a 'type' field
            customer = Customer.objects.get(user=request.user)
            return getattr(customer, 'type', 'registered')
        except Customer.DoesNotExist:
            return 'registered'  # Default for authenticated users
    
    return 'guest'  # Default for unauthenticated users

def _route_to_guest_service(request, customer_id):
    """Proxy request to guest customer service"""
    url = f"{GUEST_SERVICE_URL}/customers/{customer_id}/"
    return _forward_request(request, url)

def _route_to_registered_service(request, customer_id):
    """Proxy request to registered customer service"""
    url = f"{REGISTERED_SERVICE_URL}/customers/{customer_id}/"
    return _forward_request(request, url)

def _route_to_vip_service(request, customer_id):
    """Proxy request to VIP customer service"""
    url = f"{VIP_SERVICE_URL}/customers/{customer_id}/"
    return _forward_request(request, url)

def _route_to_guest_service_list(request):
    """Proxy request to guest customer service list endpoint"""
    url = f"{GUEST_SERVICE_URL}/customers/"
    return _forward_request(request, url)

def _route_to_registered_service_list(request):
    """Proxy request to registered customer service list endpoint"""
    url = f"{REGISTERED_SERVICE_URL}/customers/"
    return _forward_request(request, url)

def _route_to_vip_service_list(request):
    """Proxy request to VIP customer service list endpoint"""
    url = f"{VIP_SERVICE_URL}/customers/"
    return _forward_request(request, url)

def _forward_request(request, url):
    """
    Forward the request to the appropriate service and return the response
    """
    method = request.method.lower()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Copy authentication headers if present
    if 'HTTP_AUTHORIZATION' in request.META:
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']
    
    # Forward user ID if authenticated
    if request.user.is_authenticated:
        headers['X-User-ID'] = str(request.user.id)
    
    try:
        if method == 'get':
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, json=request.data, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=request.data, headers=headers)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Return the service response
        return Response(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Error forwarding request to {url}: {str(e)}")
        return Response({"error": "Service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# REST API ViewSet (keep for backward compatibility)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        form = CustomerRegistrationForm(request.data)
        if form.is_valid():
            user = form.save()
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)