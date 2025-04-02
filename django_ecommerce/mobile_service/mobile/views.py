from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Mobile
from .serializers import MobileSerializer

class MobileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Mobile model providing CRUD operations and additional endpoints
    """
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand', 'model_number', 'processor']
    ordering_fields = ['price', 'screen_size', 'ram', 'storage']
    
    @action(detail=False, methods=['get'])
    def brands(self, request):
        """
        Return a list of unique mobile brands
        """
        brands = Mobile.objects.values_list('brand', flat=True).distinct()
        return Response(list(brands))
    
    @action(detail=False, methods=['get'])
    def by_os(self, request):
        """
        Get mobile devices filtered by operating system
        """
        os_type = request.query_params.get('os_type', None)
        os_version = request.query_params.get('os_version', None)
        
        if not (os_type or os_version):
            return Response({"error": "OS type or version parameter is required"}, status=400)
        
        query = Q()
        if os_type:
            query |= Q(operating_system__iexact=os_type)
        if os_version:
            query |= Q(os_version__icontains=os_version)
            
        mobiles = self.queryset.filter(query)
        serializer = self.get_serializer(mobiles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_camera(self, request):
        """
        Get mobile devices filtered by camera specs
        """
        min_mp = request.query_params.get('min_mp', None)
        
        if not min_mp:
            return Response({"error": "Minimum megapixels parameter is required"}, status=400)
        
        try:
            min_mp_value = int(min_mp)
            # Filter devices where any rear camera has at least the specified megapixels
            mobiles = []
            for mobile in self.queryset.all():
                for camera in mobile.rear_cameras:
                    if camera.get('mp', 0) >= min_mp_value:
                        mobiles.append(mobile)
                        break
                        
            serializer = self.get_serializer(mobiles, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid megapixels value"}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_network(self, request):
        """
        Get mobile devices filtered by network type (4G/5G)
        """
        network = request.query_params.get('network', None)
        
        if not network:
            return Response({"error": "Network parameter is required"}, status=400)
        
        mobiles = self.queryset.filter(network_type__iexact=network)
        serializer = self.get_serializer(mobiles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def flagship(self, request):
        """
        Get flagship mobile devices (high-end specs)
        """
        # Flagship phones typically have high RAM, latest network, and premium features
        flagships = self.queryset.filter(
            ram__gte=8,  # At least 8GB RAM
            network_type='5g',  # 5G connectivity
            price__gte=700  # Premium price point
        )
        
        serializer = self.get_serializer(flagships, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def budget(self, request):
        """
        Get budget-friendly mobile devices
        """
        max_price = request.query_params.get('max_price', 300)
        try:
            budget_phones = self.queryset.filter(price__lte=float(max_price))
            serializer = self.get_serializer(budget_phones, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid price value"}, status=400)
    
    @action(detail=False, methods=['get'])
    def with_features(self, request):
        """
        Get mobile devices with specific features
        """
        has_nfc = request.query_params.get('nfc', '').lower() == 'true'
        has_fingerprint = request.query_params.get('fingerprint', '').lower() == 'true'
        has_face_recognition = request.query_params.get('face_recognition', '').lower() == 'true'
        has_wireless_charging = request.query_params.get('wireless_charging', '').lower() == 'true'
        
        query = Q()
        
        if has_nfc:
            query &= Q(has_nfc=True)
        if has_fingerprint:
            query &= Q(fingerprint_sensor=True)
        if has_face_recognition:
            query &= Q(face_recognition=True)
        if has_wireless_charging:
            query &= Q(wireless_charging=True)
            
        mobiles = self.queryset.filter(query)
        serializer = self.get_serializer(mobiles, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """
        Get mobile devices that are in stock
        """
        mobiles = self.queryset.filter(is_available=True, stock_quantity__gt=0)
        serializer = self.get_serializer(mobiles, many=True)
        return Response(serializer.data) 