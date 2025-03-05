import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal
from .models import Cart, CartItem
from rest_framework import viewsets
from .models import Cart
from .serializers import CartSerializer

def view_cart(request):
    # Get the user ID from the request headers
    user_id = request.META.get('HTTP_X_USER_ID')
    if not user_id:
        return HttpResponse("Unauthorized", status=401)
    
    # Fetch or create the user’s cart
    cart, _ = Cart.objects.get_or_create(customer_id=user_id)
    cart_items = []
    
    # Fetch details for each item in the cart via the gateway
    for cart_item in cart.items.all():
        response = requests.get(f'http://gateway:8000/gateway/items/{cart_item.item_id}/')
        if response.status_code == 200:
            item_data = response.json()
            cart_items.append({
                'name': item_data['name'],
                'quantity': cart_item.quantity,
                'price': cart_item.price_at_addition,
            })
        else:
            # Fallback in case the item service fails
            cart_items.append({
                'name': 'Unknown Item',
                'quantity': cart_item.quantity,
                'price': cart_item.price_at_addition,
            })
    
    return render(request, 'view_cart.html', {'cart_items': cart_items})

def add_to_cart(request, item_id):
    user_id = request.META.get('HTTP_X_USER_ID')
    if not user_id:
        return HttpResponse("Unauthorized", status=401)
    
    # Fetch item details from the items service via the gateway
    response = requests.get(f'http://gateway:8000/gateway/items/{item_id}/')
    if response.status_code != 200:
        return HttpResponse("Item not found", status=404)
    
    item_data = response.json()
    price = Decimal(item_data['price'])
    
    # Add or update the item in the cart
    cart, _ = Cart.objects.get_or_create(customer_id=user_id)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item_id=item_id,
        defaults={'quantity': 1, 'price_at_addition': price}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer