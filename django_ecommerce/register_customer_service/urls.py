from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.RegisteredCustomerViewSet, basename='registered-customer')
router.register(r'addresses', views.RegisteredAddressViewSet, basename='registered-address')

urlpatterns = [
    # Web views
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('address/add/', views.add_address_view, name='add_address'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 