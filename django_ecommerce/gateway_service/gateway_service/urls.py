from django.urls import path, include
from gateway.views import GatewayView

urlpatterns = [
    # Include all routes from the gateway app
    path('', include('gateway.urls')),
    
    # API routes for all services (keeping these for backward compatibility)
    path('gateway/<str:service>/', GatewayView.as_view(), name='gateway-list'),
    path('gateway/<str:service>/<int:pk>/', GatewayView.as_view(), name='gateway-detail'),
]