from django.urls import path, include
from rest_framework.routers import DefaultRouter
from paying.views import PaymentViewSet

router = DefaultRouter()
router.register(r'api/paying', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]