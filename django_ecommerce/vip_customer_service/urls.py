from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.VIPCustomerViewSet, basename='vip-customer')
router.register(r'addresses', views.VIPAddressViewSet, basename='vip-address')
router.register(r'benefits', views.VIPBenefitViewSet, basename='vip-benefit')
router.register(r'customer-benefits', views.VIPCustomerBenefitViewSet, basename='vip-customer-benefit')

urlpatterns = [
    # Web views
    path('', views.home_view, name='vip_home'),
    path('register/', views.register_view, name='vip_register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='vip_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='vip_logout'),
    path('dashboard/', views.vip_dashboard, name='vip_dashboard'),
    path('address/add/', views.add_address_view, name='vip_add_address'),
    path('upgrade-tier/', views.upgrade_tier_view, name='vip_upgrade_tier'),
    path('activate-benefit/<int:benefit_id>/', views.activate_benefit_view, name='vip_activate_benefit'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 