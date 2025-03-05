from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customer.views import CustomerViewSet
from cart.views import CartViewSet
from order.views import OrderViewSet
from shipping.views import ShippingViewSet
from paying.views import PaymentViewSet
from items.views import ItemViewSet

router = DefaultRouter()
router.register(r'api/customer', CustomerViewSet, basename='customer')
router.register(r'api/cart', CartViewSet, basename='cart')
router.register(r'api/order', OrderViewSet, basename='order')
router.register(r'api/shipping', ShippingViewSet, basename='shipping')
router.register(r'api/paying', PaymentViewSet, basename='paying')
router.register(r'api/items', ItemViewSet, basename='items')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('items/', include('items.urls')),
    path('cart/', include('cart.urls')),
    path('paying/', include('paying.urls')),
    path('', include('customer.urls')),
    path('', include(router.urls)),  # Include REST API routes
]