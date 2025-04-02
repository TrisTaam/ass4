from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customer.views import CustomerViewSet

router = DefaultRouter()
router.register(r'api/customer-legacy', CustomerViewSet)

urlpatterns = [
    # Include the router URLs for backward compatibility
    path('', include(router.urls)),
    
    # Include our new API endpoints from the customer app
    path('api/', include('customer.urls')),
]