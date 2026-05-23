from django.shortcuts import render

# Create your views here.
from .serializers import KycDocsSerializer,KycSerializer
from .models import KycDocs

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView


class AddDocsView(CreateAPIView):
    serializer_class=KycDocsSerializer
    
    def get_queryset(self):
        return KycDocs.objects.filter(user=self.request.user)
    def get_serializer_context(self):
        return {'request': self.request}
    
    
class ListDocsView(ListAPIView): 
    serializer_class=KycSerializer
    
    def get_queryset(self):
        return KycDocs.objects.filter(user=self.request.user)
    