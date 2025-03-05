from django.urls import path
from gateway.views import GatewayView

urlpatterns = [
    path('gateway/<str:service>/', GatewayView.as_view(), name='gateway-list'),
    path('gateway/<str:service>/<int:pk>/', GatewayView.as_view(), name='gateway-detail'),
]