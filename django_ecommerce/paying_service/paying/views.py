import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Payment
from django.utils import timezone
from rest_framework import viewsets
from .serializers import PaymentSerializer

def checkout(request):
    user_id = request.META.get('HTTP_X_USER_ID')
    if not user_id:
        return HttpResponse("Unauthorized", status=401)
    
    # Fetch cart data via the gateway
    cart_response = requests.get(f'http://gateway:8000/gateway/cart/', headers={'X-User-ID': user_id})
    if cart_response.status_code != 200:
        return HttpResponse("Cart not found", status=404)
    
    cart_data = cart_response.json()[0]  # Assuming one cart per user
    total_price = sum(float(item['price_at_addition']) * item['quantity'] for item in cart_data['items'])
    
    if request.method == 'POST':
        # Create an order via the gateway
        order_data = {
            'customer_id': user_id,
            'total_price': str(total_price),
            'shipping_address': {'address': 'Sample Address'},
            'items': [
                {'item_id': item['item_id'], 'quantity': item['quantity'], 'price': str(item['price_at_addition'])}
                for item in cart_data['items']
            ]
        }
        order_response = requests.post(
            'http://gateway:8000/gateway/orders/',
            json=order_data,
            headers={'X-User-ID': user_id}
        )
        if order_response.status_code != 201:
            return HttpResponse("Failed to create order", status=400)
        
        order_id = order_response.json()['id']
        
        # Create shipping record via the gateway
        shipping_data = {
            'order': order_id,
            'shipping_method': 'standard',
            'shipping_cost': '5.00'
        }
        requests.post(
            'http://gateway:8000/gateway/shipping/',
            json=shipping_data,
            headers={'X-User-ID': user_id}
        )
        
        # Create payment record
        Payment.objects.create(
            order_id=order_id,
            payment_method='credit_card',
            amount=total_price,
            status='completed',
            paid_at=timezone.now()
        )
        
        # Clear the cart via the gateway
        requests.delete(f'http://gateway:8000/gateway/cart/', headers={'X-User-ID': user_id})
        return redirect('success')
    
    return render(request, 'checkout.html', {'total_price': total_price})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer