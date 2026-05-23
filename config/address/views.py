from django.shortcuts import render
from .models import Address
from .serializers import AddressSerializer 
from accounts.models import User

from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsActiveUsers

class AddressView(ModelViewSet):
    
    permission_classes =[IsActiveUsers]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    serializer_class = AddressSerializer
    
    