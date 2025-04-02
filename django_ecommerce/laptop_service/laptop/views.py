from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Laptop
from .serializers import LaptopSerializer

class LaptopViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Laptop model providing CRUD operations and additional endpoints
    """
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'processor_model', 'operating_system']
    ordering_fields = ['price', 'screen_size', 'ram', 'storage_capacity']
    
    @action(detail=False, methods=['get'])
    def brands(self, request):
        """
        Return a list of unique laptop brands
        """
        brands = Laptop.objects.values_list('brand', flat=True).distinct()
        return Response(list(brands))
    
    @action(detail=False, methods=['get'])
    def by_processor(self, request):
        """
        Get laptops filtered by processor brand/model
        """
        processor_brand = request.query_params.get('brand', None)
        processor_model = request.query_params.get('model', None)
        
        if not (processor_brand or processor_model):
            return Response({"error": "Processor brand or model parameter is required"}, status=400)
        
        query = Q()
        if processor_brand:
            query |= Q(processor_brand__icontains=processor_brand)
        if processor_model:
            query |= Q(processor_model__icontains=processor_model)
            
        laptops = self.queryset.filter(query)
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_specs(self, request):
        """
        Get laptops filtered by RAM, storage, and screen size
        """
        min_ram = request.query_params.get('min_ram', None)
        min_storage = request.query_params.get('min_storage', None)
        min_screen = request.query_params.get('min_screen', None)
        
        query = Q()
        
        if min_ram:
            try:
                query &= Q(ram__gte=int(min_ram))
            except ValueError:
                pass
        
        if min_storage:
            try:
                query &= Q(storage_capacity__gte=int(min_storage))
            except ValueError:
                pass
                
        if min_screen:
            try:
                query &= Q(screen_size__gte=float(min_screen))
            except ValueError:
                pass
        
        laptops = self.queryset.filter(query)
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def gaming(self, request):
        """
        Get laptops suitable for gaming (high specs)
        """
        # Gaming laptops typically have dedicated graphics and high RAM
        laptops = self.queryset.filter(
            ram__gte=16,  # At least 16GB RAM
            graphics_memory__gte=4  # At least 4GB graphics memory
        ).exclude(
            graphics_card__icontains='integrated'  # Exclude integrated graphics
        )
        
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def business(self, request):
        """
        Get laptops suitable for business use
        """
        # Business laptops typically prioritize battery life, portability
        laptops = self.queryset.filter(
            battery_life__gte=8,  # At least 8 hours battery
            weight__lte=2.0  # Less than 2 kg
        )
        
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """
        Get laptops that are in stock
        """
        laptops = self.queryset.filter(is_available=True, stock_quantity__gt=0)
        serializer = self.get_serializer(laptops, many=True)
        return Response(serializer.data) 