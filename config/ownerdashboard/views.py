from django.shortcuts import render
from products.models import Product
from products.serializers import ProductSerializer
from products.pagination import CustomPagination
from rest_framework.viewsets import ModelViewSet
from products.utils import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerUser,IsOwnerDashboardUser
from booking.models import Booking,Booked_items
from  booking.serializers import BookingSerializer
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import OwnerBookingStatusUpdateSerializer,OwnerBookedItemsSerializer
from accounts.permissions import IsActiveUsers

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
    return Booked_items.objects.filter(
        product__owner=user 
    ).select_related('booking', 'booking__user','product').distinct()
    #  .prefetch_related('items__product')\
    
class OwnerOrdersListView(ModelViewSet):
    # permission_classes =[IsOwnerUser]
    permission_classes = [IsOwnerDashboardUser]
    
    
    # serializer_class = BookingSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Optional filters
    filterset_fields = ['status', 'deposit_status']
    search_fields = ['booking__user__email','product__title']
    ordering_fields = ['created_at', 'total_rent_money']
    ordering = ['-created_at']
    
    def get_queryset(self): 
        user = self.request.user
        
        return get_owner_orders(user)
    
    def get_serializer_class(self):
        if self.action in ['update','partial_update']:
            return OwnerBookingStatusUpdateSerializer
        return OwnerBookedItemsSerializer
    
from django.db.models import Q



class OwnerDashboardStatsView(APIView):

    # permission_classes = [IsOwnerUser]
    permission_classes = [IsOwnerDashboardUser]
    

    def get(self, request):

        user = request.user

        items = Booked_items.objects.filter(
            product__owner=user
        )

        stats = items.aggregate(

            total_orders=Count('id'),

            total_revenue=Sum(
                'booking__total_rent_money',
                filter=Q(
                    status__in=['DELIVERED', 'RETURNED']
                )
            )
        )

        return Response({

            'total_orders': stats['total_orders'] or 0,

            'total_revenue': stats['total_revenue'] or 0
        })