import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from django.shortcuts import render, redirect

def login_view(request):
    # If the user is already authenticated, redirect to home or profile
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

def register_view(request):
    # Handle the registration logic, or just render the registration page
    if request.method == 'POST':
        # Add registration logic here (e.g., saving user data)
        return redirect('login')  # Redirect to login after successful registration
    return render(request, 'register.html')

def profile_view(request):
    # Render the profile page
    if not request.user.is_authenticated:
        return redirect('login')  # If not authenticated, redirect to login
    return render(request, 'profile.html', {'user': request.user})

def home_view(request):
    # Render the home page
    return render(request, 'home.html')


class GatewayView(APIView):
    # Dictionary mapping service names to their internal URLs
    service_urls = {
        'customers': 'http://customer:8001/api/customer/',
        'items': 'http://items:8005/api/items/',
        'cart': 'http://cart:8002/api/cart/',
        'orders': 'http://order:8003/api/order/',
        'payments': 'http://paying:8004/api/paying/',
        'shipping': 'http://shipping:8006/api/shipping/',
    }

    def get(self, request, service, pk=None):
        if service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        
        url = f"{self.service_urls[service]}{pk}/" if pk else self.service_urls[service]
        headers = {'X-User-ID': request.META.get('HTTP_X_USER_ID', '')}
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
        if service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        
        headers = {'X-User-ID': request.META.get('HTTP_X_USER_ID', '')}
        response = requests.post(self.service_urls[service], json=request.data, headers=headers)
        return Response(response.json(), status=response.status_code)

    # Add similar methods for PUT, DELETE, etc., as needed
    def put(self, request, service, pk):
        if service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        
        url = f"{self.service_urls[service]}{pk}/"
        headers = {'X-User-ID': request.META.get('HTTP_X_USER_ID', '')}
        response = requests.put(url, json=request.data, headers=headers)
        return Response(response.json(), status=response.status_code)

    def delete(self, request, service, pk):
        if service not in self.service_urls:
            return Response({"error": "Service not found"}, status=404)
        
        url = f"{self.service_urls[service]}{pk}/"
        headers = {'X-User-ID': request.META.get('HTTP_X_USER_ID', '')}
        response = requests.delete(url, headers=headers)
        return Response(response.status_code, status=response.status_code)