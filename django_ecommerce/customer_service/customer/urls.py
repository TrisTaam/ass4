from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Main customer endpoints
    path('customer/<int:customer_id>/', views.customer_detail, name='customer-detail'),
    path('customer/', views.customer_list, name='customer-list'),
    
    # Specific customer service endpoints that will be proxied
    path('guest-customer/<int:customer_id>/', views.guest_customer_detail, name='guest-customer-detail'),
    path('registered-customer/<int:customer_id>/', views.registered_customer_detail, name='registered-customer-detail'),
    path('vip-customer/<int:customer_id>/', views.vip_customer_detail, name='vip-customer-detail'),
]