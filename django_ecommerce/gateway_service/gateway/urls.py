from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GatewayView
from gateway import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # Default route redirect to home
    path('', RedirectView.as_view(url='/home/', permanent=False), name='index'),
    
    # Serve UI pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),
    
    # API routes for all services
    path('api/<str:service>/', GatewayView.as_view(), name='gateway-list'),
    path('api/<str:service>/<int:pk>/', GatewayView.as_view(), name='gateway-detail'),
]
