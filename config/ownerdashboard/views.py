from django.shortcuts import render
from products.models import Product
from products.serializers import ProductSerializer
from products.pagination import CustomPagination
from rest_framework.viewsets import ModelViewSet
from products.utils import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerUser
from booking.models import Booking
from  booking.serializers import BookingSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response


#owner products api

class OwnerProductView(ModelViewSet):
    
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes =[IsOwnerUser]

    filter_backends=[DjangoFilterBackend,
                     SearchFilter,
                     OrderingFilter
                     
                     ]
    # filterset_fields= ['category_name','price_per_day','title']
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['price_per_day','brand_name']
    ordering = ['brand_name']

    def get_queryset(self):
        return Product.objects.select_related('owner', 'category').filter(owner=self.request.user)
    
    
# owner get orders

def get_owner_orders(user):
    return Booking.objects.filter(
        items__product__owner =user
    ).select_related('user','address').prefetch_related('items').distinct()
    
    
class OwnerOrdersListView(ModelViewSet):
    permission_classes =[IsOwnerUser]
    
    serializer_class = BookingSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Optional filters
    filterset_fields = ['status', 'deposit_status']
    search_fields = ['user__email']
    ordering_fields = ['created_at', 'total_rent_money']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        
        return get_owner_orders(user)
    
class OwnerDashboardStatsView(APIView):
    
    def get(self,request):
        user = request.user
        
        orders = get_owner_orders(user)
        
        total_orders = orders.count()
        
        revenue = orders.filter(
            status='pending'
        ).aggregate(total = Sum('total_rent_money'))['total'] or  0
        
        return Response(
            {
                'total_orders':total_orders,
                'total_revenue':revenue
            }
        )