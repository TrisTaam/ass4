from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GatewayView
from gateway import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # Default route points directly to home view
    path('', views.home_view, name='index'),
    
    # Serve UI pages
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),
    
    # Product pages
    path('products/', views.product_list_view, name='product-list'),
    path('products/<str:category>/', views.product_list_view, name='product-list-category'),
    path('product/<int:product_id>/', views.product_detail_view, name='product-detail'),
    
    # Shopping cart and checkout
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    # API routes for all services
    path('api/<str:service>/', GatewayView.as_view(), name='gateway-list'),
    path('api/<str:service>/<int:pk>/', GatewayView.as_view(), name='gateway-detail'),
    
    # Direct routes to specific services
    path('api/customers/', GatewayView.as_view(), {'service': 'customers'}, name='customers-list'),
    path('api/customers/<int:pk>/', GatewayView.as_view(), {'service': 'customers'}, name='customers-detail'),
    
    path('api/items/', GatewayView.as_view(), {'service': 'items'}, name='items-list'),
    path('api/items/<int:pk>/', GatewayView.as_view(), {'service': 'items'}, name='items-detail'),
    
    # Type-specific item routes
    path('api/items/books/', GatewayView.as_view(), {'service': 'books'}, name='books-list'),
    path('api/items/laptops/', GatewayView.as_view(), {'service': 'laptops'}, name='laptops-list'),
    path('api/items/mobiles/', GatewayView.as_view(), {'service': 'mobiles'}, name='mobiles-list'),
    path('api/items/clothes/', GatewayView.as_view(), {'service': 'clothes'}, name='clothes-list'),
    
    # Type-specific customer routes
    path('api/guest-customers/', GatewayView.as_view(), {'service': 'guest-customers'}, name='guest-customers-list'),
    path('api/registered-customers/', GatewayView.as_view(), {'service': 'registered-customers'}, name='registered-customers-list'),
    path('api/vip-customers/', GatewayView.as_view(), {'service': 'vip-customers'}, name='vip-customers-list'),
]
