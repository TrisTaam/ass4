from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GatewayViewSet
from gateway import views

router = DefaultRouter()
router.register(r'gateway/(?P<service>[^/.]+)', GatewayViewSet, basename='gateway')

urlpatterns = [
    # Serve UI pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),
    
    # API Routes - Reverse proxy to the respective service
    path('api/customer/', include('customer.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/items/', include('items.urls')),
    path('api/order/', include('order.urls')),
    path('api/shipping/', include('shipping.urls')),
    path('api/paying/', include('paying.urls')),
]