#!/usr/bin/env python

def update_gateway_views():
    gateway_views_path = 'django_ecommerce/gateway_service/gateway/views.py'
    
    new_content = '''import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render, redirect

def login_view(request):
    # If the user is already authenticated, redirect to home or profile
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "login.html")

def register_view(request):
    # Handle the registration logic, or just render the registration page
    if request.method == "POST":
        # Add registration logic here (e.g., saving user data)
        return redirect("login")  # Redirect to login after successful registration
    return render(request, "register.html")

def profile_view(request):
    # Render the profile page
    if not request.user.is_authenticated:
        return redirect("login")  # If not authenticated, redirect to login
    return render(request, "profile.html", {"user": request.user})

def home_view(request):
    # Render the home page
    return render(request, "home.html")

class GatewayView(APIView):
    # Dictionary mapping service names to their internal URLs
    service_urls = {
        "items": "http://items:8005/api/items/",
        "cart": "http://cart:8002/api/cart/",
        "orders": "http://order:8003/api/order/",
        "payments": "http://paying:8004/api/paying/",
        "shipping": "http://shipping:8006/api/shipping/",
    }
    
    # Customer service URLs based on customer type
    customer_service_urls = {
        "guest": "http://guest-customer:8001/api/",
        "registered": "http://register-customer:8007/api/",
        "vip": "http://vip-customer:8008/api/",
    }

    def _get_customer_service_url(self, request):
        """Determine which customer service to route to based on user status and type"""
        # Check if there is an authenticated user
        user_id = request.META.get("HTTP_X_USER_ID", "")
        
        if not user_id:
            # If no user ID, use guest customer service
            return self.customer_service_urls["guest"]
        
        # Check customer type from the header if provided
        customer_type = request.META.get("HTTP_X_CUSTOMER_TYPE", "")
        
        if customer_type in self.customer_service_urls:
            return self.customer_service_urls[customer_type]
        
        # Default to registered customer if type not specified but user exists
        return self.customer_service_urls["registered"]

    def get(self, request, service, pk=None):
        # Special handling for customer service routing
        if service == "customers":
            base_url = self._get_customer_service_url(request)
            url = f"{base_url}customers/{pk}/" if pk else f"{base_url}customers/"
        elif service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        else:
            url = f"{self.service_urls[service]}{pk}/" if pk else self.service_urls[service]
        
        headers = {
            "X-User-ID": request.META.get("HTTP_X_USER_ID", ""),
            "X-Customer-Type": request.META.get("HTTP_X_CUSTOMER_TYPE", "")
        }
        
        response = requests.get(url, headers=headers)
        
        # Debugging output
        print(f"Request URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        try:
            return Response(response.json(), status=response.status_code)
        except ValueError:
            return Response(
                {"error": "Invalid JSON response", "content": response.text},
                status=500
            )

    def post(self, request, service):
        # Special handling for customer service routing
        if service == "customers":
            base_url = self._get_customer_service_url(request)
            url = f"{base_url}customers/"
        elif service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        else:
            url = self.service_urls[service]
        
        headers = {
            "X-User-ID": request.META.get("HTTP_X_USER_ID", ""),
            "X-Customer-Type": request.META.get("HTTP_X_CUSTOMER_TYPE", "")
        }
        
        response = requests.post(url, json=request.data, headers=headers)
        return Response(response.json(), status=response.status_code)

    def put(self, request, service, pk):
        # Special handling for customer service routing
        if service == "customers":
            base_url = self._get_customer_service_url(request)
            url = f"{base_url}customers/{pk}/"
        elif service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        else:
            url = f"{self.service_urls[service]}{pk}/"
        
        headers = {
            "X-User-ID": request.META.get("HTTP_X_USER_ID", ""),
            "X-Customer-Type": request.META.get("HTTP_X_CUSTOMER_TYPE", "")
        }
        
        response = requests.put(url, json=request.data, headers=headers)
        return Response(response.json(), status=response.status_code)

    def delete(self, request, service, pk):
        # Special handling for customer service routing
        if service == "customers":
            base_url = self._get_customer_service_url(request)
            url = f"{base_url}customers/{pk}/"
        elif service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        else:
            url = f"{self.service_urls[service]}{pk}/"
        
        headers = {
            "X-User-ID": request.META.get("HTTP_X_USER_ID", ""),
            "X-Customer-Type": request.META.get("HTTP_X_CUSTOMER_TYPE", "")
        }
        
        response = requests.delete(url, headers=headers)
        return Response(status=response.status_code)
'''

    with open(gateway_views_path, 'w') as f:
        f.write(new_content)
    
    print(f"Successfully updated {gateway_views_path}")

def update_gateway_urls():
    gateway_urls_path = 'django_ecommerce/gateway_service/gateway/urls.py'
    
    new_content = '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GatewayView
from gateway import views

urlpatterns = [
    # Serve UI pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),
    
    # API routes for all services
    path('api/<str:service>/', GatewayView.as_view(), name='gateway-list'),
    path('api/<str:service>/<int:pk>/', GatewayView.as_view(), name='gateway-detail'),
    
    # Direct routes to customer services
    path('guest/', include('guest_customer_service.urls')),
    path('register/', include('register_customer_service.urls')),
    path('vip/', include('vip_customer_service.urls')),
]
'''

    with open(gateway_urls_path, 'w') as f:
        f.write(new_content)
    
    print(f"Successfully updated {gateway_urls_path}")

if __name__ == "__main__":
    print("Updating gateway service files...")
    update_gateway_views()
    update_gateway_urls()
    print("Gateway service files updated successfully!") 