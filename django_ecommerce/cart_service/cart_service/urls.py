from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet

router = DefaultRouter()
router.register(r'api/cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]