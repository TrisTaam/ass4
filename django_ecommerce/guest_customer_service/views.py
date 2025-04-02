from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import GuestCustomer, GuestAddress
from .serializers import GuestCustomerSerializer, GuestAddressSerializer
import uuid

# Web view for guest customers
def guest_home(request):
    # Check if a session exists for the guest
    session_id = request.session.get('guest_session_id')
    
    # If no session exists, create one
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['guest_session_id'] = session_id
        
        # Create a guest customer record in the database
        GuestCustomer.objects.create(session_id=session_id)
    
    return render(request, 'guest_home.html', {'session_id': session_id})

# API ViewSet for guest customers
class GuestCustomerViewSet(viewsets.ModelViewSet):
    queryset = GuestCustomer.objects.all()
    serializer_class = GuestCustomerSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def create_guest(self, request):
        # Generate a unique session ID for the guest
        session_id = str(uuid.uuid4())
        guest = GuestCustomer.objects.create(session_id=session_id)
        serializer = self.get_serializer(guest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        guest = self.get_object()
        data = request.data.copy()
        data['guest_customer'] = guest.id
        
        serializer = GuestAddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
