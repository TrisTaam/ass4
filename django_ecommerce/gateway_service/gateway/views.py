import requests
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
        "books": "http://book-service:8010/api/books/",
        "laptops": "http://laptop-service:8011/api/laptops/",
        "mobiles": "http://mobile-service:8012/api/mobiles/",
        "clothes": "http://clothes-service:8013/api/clothes/",
        "cart": "http://cart:8002/api/cart/",
        "orders": "http://order:8003/api/order/",
        "payments": "http://paying:8004/api/paying/",
        "shipping": "http://shipping:8006/api/shipping/",
        "customers": "http://customer-service:8009/api/customer/",  # Route through customer service router
    }
    
    # Customer service URLs based on customer type
    customer_service_urls = {
        "guest": "http://guest-customer:8001/api/",
        "registered": "http://register-customer:8007/api/",
        "vip": "http://vip-customer:8008/api/",
    }

    def _get_customer_service_url(self, request):
        """Determine which customer service to route to based on user status and type"""
        # Modified to use the customer service router for all customer requests
        return "http://customer-service:8009/api/"

    def get(self, request, service, pk=None):
        # Special handling for customer service routing
        if service == "customers":
            base_url = self._get_customer_service_url(request)
            url = f"{base_url}customer/{pk}/" if pk else f"{base_url}customer/"
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
            url = f"{base_url}customer/"
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
            url = f"{base_url}customer/{pk}/"
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
            url = f"{base_url}customer/{pk}/"
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
