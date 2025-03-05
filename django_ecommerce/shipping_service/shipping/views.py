from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Shipping
from .serializers import ShippingSerializer

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Shipping.objects.filter(order__customer_id=self.request.user.id)