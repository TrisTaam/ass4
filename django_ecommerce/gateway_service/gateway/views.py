import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

def login_view(request):
    # If the user is already authenticated, redirect to home or profile
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

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

def product_list_view(request, category=None):
    # Render the product list page, optionally filtered by category
    context = {'category': category} if category else {}
    return render(request, 'product_list.html', context)

def product_detail_view(request, product_id):
    # Render the product detail page
    return render(request, 'product_detail.html', {'product_id': product_id})

def cart_view(request):
    # Render the cart page
    return render(request, 'cart.html')

def checkout_view(request):
    # Render the checkout page
    return render(request, 'checkout.html')

class GatewayView(APIView):
    # Dictionary mapping service names to their internal URLs
    service_urls = {
        # Customer services
        'customers': 'http://customer-service:8001/api/customers/',
        'guest-customers': 'http://guest-customer:8001/api/guest-customers/',
        'registered-customers': 'http://register-customer:8007/api/registered-customers/',
        'vip-customers': 'http://vip-customer:8008/api/vip-customers/',
        
        # Item services
        'items': 'http://items-service:8005/api/items/',
        'books': 'http://book-service:8010/api/books/',
        'laptops': 'http://laptop-service:8011/api/laptops/',
        'mobiles': 'http://mobile-service:8012/api/mobiles/',
        'clothes': 'http://clothes-service:8013/api/clothes/',
        
        # Other services
        'cart': 'http://cart-service:8002/api/cart/',
        'orders': 'http://order-service:8003/api/order/',
        'payments': 'http://paying-service:8004/api/paying/',
        'shipping': 'http://shipping-service:8006/api/shipping/',
    }
    
    def _forward_request(self, request, url, pk=None):
        """
        Forward the request to the appropriate service and return the response
        """
        if pk:
            url = f"{url}{pk}/"
            
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
            
            # Add customer type if available
            if hasattr(request.user, 'customer') and hasattr(request.user.customer, 'type'):
                headers['X-Customer-Type'] = request.user.customer.type
        
        try:
            if method == 'get':
                response = requests.get(url, headers=headers, params=request.query_params)
            elif method == 'post':
                response = requests.post(url, json=request.data, headers=headers)
            elif method == 'put':
                response = requests.put(url, json=request.data, headers=headers)
            elif method == 'patch':
                response = requests.patch(url, json=request.data, headers=headers)
            elif method == 'delete':
                response = requests.delete(url, headers=headers)
            else:
                return Response({"error": "Method not allowed"}, status=405)
            
            # Return the service response
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error forwarding request to {url}: {str(e)}")
            return Response({"error": "Service unavailable"}, status=503)

    def get(self, request, service, pk=None):
        """Handle GET requests to services"""
        if service not in self.service_urls:
            return Response({"error": f"Unknown service: {service}"}, status=404)
            
        return self._forward_request(request, self.service_urls[service], pk)
        
    def post(self, request, service, pk=None):
        """Handle POST requests to services"""
        if service not in self.service_urls:
            return Response({"error": f"Unknown service: {service}"}, status=404)
            
        return self._forward_request(request, self.service_urls[service], pk)
        
    def put(self, request, service, pk=None):
        """Handle PUT requests to services"""
        if service not in self.service_urls:
            return Response({"error": f"Unknown service: {service}"}, status=404)
            
        return self._forward_request(request, self.service_urls[service], pk)
        
    def patch(self, request, service, pk=None):
        """Handle PATCH requests to services"""
        if service not in self.service_urls:
            return Response({"error": f"Unknown service: {service}"}, status=404)
            
        return self._forward_request(request, self.service_urls[service], pk)
        
    def delete(self, request, service, pk=None):
        """Handle DELETE requests to services"""
        if service not in self.service_urls:
            return Response({"error": f"Unknown service: {service}"}, status=404)
            
        return self._forward_request(request, self.service_urls[service], pk)