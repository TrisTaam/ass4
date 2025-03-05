from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Item
from .serializers import ItemSerializer
from bson import ObjectId 
from rest_framework.exceptions import NotFound

# Traditional views
def home(request):
    items = Item.objects.all()[:10]
    return render(request, 'home.html', {'items': items})

def item_detail(request, id):
    item = Item.objects.get(_id=ObjectId(id))
    return render(request, 'item_detail.html', {'item': item})

# REST API ViewSet
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')  # Get the ID from the URL
        try:
            # Convert the string ID to ObjectId and query the item
            obj = Item.objects.get(_id=ObjectId(pk))
        except Item.DoesNotExist:
            raise NotFound(detail="Item not found")
        self.check_object_permissions(self.request, obj)
        return obj