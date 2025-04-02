from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Item
from .serializers import ItemSerializer
from bson import ObjectId 
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

# Traditional views
def home(request):
    items = Item.objects.all()[:10]
    return render(request, 'home.html', {'items': items})

def item_detail(request, id):
    item = Item.objects.get(_id=ObjectId(id))
    return render(request, 'item_detail.html', {'item': item})

# Service URLs for specialized item services
BOOK_SERVICE_URL = "http://book-service:8010/api/books/"
LAPTOP_SERVICE_URL = "http://laptop-service:8011/api/laptops/"
MOBILE_SERVICE_URL = "http://mobile-service:8012/api/mobiles/"
CLOTHES_SERVICE_URL = "http://clothes-service:8013/api/clothes/"

class ItemViewSet(viewsets.ViewSet):
    """
    Router ViewSet that forwards requests to specialized item services
    based on item type.
    
    This service acts purely as a router and does not store item data itself.
    All data is stored and managed by the specialized services.
    """
    
    def list(self, request):
        """
        List all items by aggregating results from all specialized services,
        or route to a specific service based on type parameter
        """
        # Check if a specific type is requested
        item_type = request.query_params.get('type', None)
        
        if item_type == 'book':
            # Forward to book service
            return self._forward_to_service(BOOK_SERVICE_URL, request.query_params)
        elif item_type == 'laptop':
            # Forward to laptop service
            return self._forward_to_service(LAPTOP_SERVICE_URL, request.query_params)
        elif item_type == 'mobile':
            # Forward to mobile service
            return self._forward_to_service(MOBILE_SERVICE_URL, request.query_params)
        elif item_type == 'clothes':
            # Forward to clothes service
            return self._forward_to_service(CLOTHES_SERVICE_URL, request.query_params)
        
        # If no specific type, combine results from all services
        try:
            # Get items from each service
            books_response = requests.get(BOOK_SERVICE_URL)
            laptops_response = requests.get(LAPTOP_SERVICE_URL)
            mobiles_response = requests.get(MOBILE_SERVICE_URL)
            clothes_response = requests.get(CLOTHES_SERVICE_URL)
            
            # Combine results
            combined_items = []
            
            if books_response.status_code == 200:
                for item in books_response.json().get('results', []):
                    item['type'] = 'book'
                    combined_items.append(item)
                    
            if laptops_response.status_code == 200:
                for item in laptops_response.json().get('results', []):
                    item['type'] = 'laptop'
                    combined_items.append(item)
                    
            if mobiles_response.status_code == 200:
                for item in mobiles_response.json().get('results', []):
                    item['type'] = 'mobile'
                    combined_items.append(item)
                    
            if clothes_response.status_code == 200:
                for item in clothes_response.json().get('results', []):
                    item['type'] = 'clothes'
                    combined_items.append(item)
            
            return Response({
                'count': len(combined_items),
                'results': combined_items
            })
        except requests.RequestException as e:
            return Response({"detail": f"Service unavailable: {str(e)}"}, status=503)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve an item by forwarding the request to the appropriate specialized service.
        The item type is determined by trying each service.
        """
        # Try book service
        try:
            response = requests.get(f"{BOOK_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                data = response.json()
                data['type'] = 'book'
                return Response(data)
        except requests.RequestException:
            pass
        
        # Try laptop service
        try:
            response = requests.get(f"{LAPTOP_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                data = response.json()
                data['type'] = 'laptop'
                return Response(data)
        except requests.RequestException:
            pass
        
        # Try mobile service
        try:
            response = requests.get(f"{MOBILE_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                data = response.json()
                data['type'] = 'mobile'
                return Response(data)
        except requests.RequestException:
            pass
        
        # Try clothes service
        try:
            response = requests.get(f"{CLOTHES_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                data = response.json()
                data['type'] = 'clothes'
                return Response(data)
        except requests.RequestException:
            pass
        
        # If item not found in any service
        return Response({"detail": "Item not found."}, status=404)
    
    def create(self, request):
        """
        Create an item by forwarding the request to the appropriate specialized service
        based on the item type in the request data.
        """
        item_type = request.data.get('type', None)
        
        if not item_type:
            return Response({"detail": "Item type is required."}, status=400)
        
        if item_type == 'book':
            return self._forward_post_to_service(BOOK_SERVICE_URL, request.data)
        elif item_type == 'laptop':
            return self._forward_post_to_service(LAPTOP_SERVICE_URL, request.data)
        elif item_type == 'mobile':
            return self._forward_post_to_service(MOBILE_SERVICE_URL, request.data)
        elif item_type == 'clothes':
            return self._forward_post_to_service(CLOTHES_SERVICE_URL, request.data)
        else:
            return Response({"detail": f"Unsupported item type: {item_type}"}, status=400)
    
    def update(self, request, pk=None):
        """
        Update an item by forwarding the request to the appropriate specialized service.
        First determines the item type by checking each service.
        """
        item_type = request.data.get('type', None)
        
        if item_type:
            # If type is provided in the request, use it to route
            if item_type == 'book':
                return self._forward_put_to_service(f"{BOOK_SERVICE_URL}{pk}/", request.data)
            elif item_type == 'laptop':
                return self._forward_put_to_service(f"{LAPTOP_SERVICE_URL}{pk}/", request.data)
            elif item_type == 'mobile':
                return self._forward_put_to_service(f"{MOBILE_SERVICE_URL}{pk}/", request.data)
            elif item_type == 'clothes':
                return self._forward_put_to_service(f"{CLOTHES_SERVICE_URL}{pk}/", request.data)
            else:
                return Response({"detail": f"Unsupported item type: {item_type}"}, status=400)
        
        # If type not provided, try to find the item in each service
        
        # Try book service first
        try:
            response = requests.get(f"{BOOK_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_put_to_service(f"{BOOK_SERVICE_URL}{pk}/", request.data)
        except requests.RequestException:
            pass
        
        # Try laptop service
        try:
            response = requests.get(f"{LAPTOP_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_put_to_service(f"{LAPTOP_SERVICE_URL}{pk}/", request.data)
        except requests.RequestException:
            pass
        
        # Try mobile service
        try:
            response = requests.get(f"{MOBILE_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_put_to_service(f"{MOBILE_SERVICE_URL}{pk}/", request.data)
        except requests.RequestException:
            pass
        
        # Try clothes service
        try:
            response = requests.get(f"{CLOTHES_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_put_to_service(f"{CLOTHES_SERVICE_URL}{pk}/", request.data)
        except requests.RequestException:
            pass
        
        # If item not found in any service
        return Response({"detail": "Item not found."}, status=404)
    
    def destroy(self, request, pk=None):
        """
        Delete an item by forwarding the request to the appropriate specialized service.
        First determines the item type by checking each service.
        """
        # Try book service first
        try:
            response = requests.get(f"{BOOK_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_delete_to_service(f"{BOOK_SERVICE_URL}{pk}/")
        except requests.RequestException:
            pass
        
        # Try laptop service
        try:
            response = requests.get(f"{LAPTOP_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_delete_to_service(f"{LAPTOP_SERVICE_URL}{pk}/")
        except requests.RequestException:
            pass
        
        # Try mobile service
        try:
            response = requests.get(f"{MOBILE_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_delete_to_service(f"{MOBILE_SERVICE_URL}{pk}/")
        except requests.RequestException:
            pass
        
        # Try clothes service
        try:
            response = requests.get(f"{CLOTHES_SERVICE_URL}{pk}/")
            if response.status_code == 200:
                return self._forward_delete_to_service(f"{CLOTHES_SERVICE_URL}{pk}/")
        except requests.RequestException:
            pass
        
        # If item not found in any service
        return Response({"detail": "Item not found."}, status=404)
    
    @action(detail=False, methods=['get'])
    def books(self, request):
        """Get all books by forwarding to book service"""
        return self._forward_to_service(BOOK_SERVICE_URL, request.query_params)
    
    @action(detail=False, methods=['get'])
    def laptops(self, request):
        """Get all laptops by forwarding to laptop service"""
        return self._forward_to_service(LAPTOP_SERVICE_URL, request.query_params)
    
    @action(detail=False, methods=['get'])
    def mobiles(self, request):
        """Get all mobile devices by forwarding to mobile service"""
        return self._forward_to_service(MOBILE_SERVICE_URL, request.query_params)
    
    @action(detail=False, methods=['get'])
    def clothes(self, request):
        """Get all clothing items by forwarding to clothes service"""
        return self._forward_to_service(CLOTHES_SERVICE_URL, request.query_params)
    
    # Helper methods for forwarding requests
    def _forward_to_service(self, url, params=None):
        """Forward GET request to a service and return the response"""
        try:
            response = requests.get(url, params=params)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"detail": f"Service unavailable: {str(e)}"}, status=503)
    
    def _forward_post_to_service(self, url, data):
        """Forward POST request to a service and return the response"""
        try:
            response = requests.post(url, json=data)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"detail": f"Service unavailable: {str(e)}"}, status=503)
    
    def _forward_put_to_service(self, url, data):
        """Forward PUT request to a service and return the response"""
        try:
            response = requests.put(url, json=data)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({"detail": f"Service unavailable: {str(e)}"}, status=503)
    
    def _forward_delete_to_service(self, url):
        """Forward DELETE request to a service and return the response"""
        try:
            response = requests.delete(url)
            return Response(status=response.status_code)
        except requests.RequestException as e:
            return Response({"detail": f"Service unavailable: {str(e)}"}, status=503)