from django.urls import path, include
from rest_framework.routers import DefaultRouter
from items.views import ItemViewSet

router = DefaultRouter()
router.register(r'api/items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]