from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'guest-customers', views.GuestCustomerViewSet, basename='guest-customer')

urlpatterns = [
    path('', views.guest_home, name='guest_home'),
    path('api/', include(router.urls)),
] 