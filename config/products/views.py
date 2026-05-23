from django.shortcuts import render
from .models import Product,Category
from .serializers import CategorySerializer,ProductSerializer
from .pagination import CustomPagination
# from .utils import invalidate_product_cache

from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,ListCreateAPIView

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from rest_framework.response import Response
from .utils import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter


# Normal users
class ProductView(ListAPIView):
    
     
    permission_classes = [AllowAny]
    authentication_classes =[]
    
    serializer_class=ProductSerializer
    pagination_class = CustomPagination
    filter_backends=[DjangoFilterBackend,
                     SearchFilter,
                     OrderingFilter
                     
                     ]
    filterset_class = ProductFilter
    search_fields = ['title','locality']
    ordering_fields = ['price_per_day','brand_name']
    ordering = ['brand_name']
    
    def get_queryset(self):
        return  Product.objects.select_related('owner','category').filter(is_active = True,owner__is_live=True)
         
    
    
    
    
    def list(self,request,*args,**kwargs):
        version = cache.get('product_version',1)
        # page = request.query_params.get('page', 1)

        # cache_key = f"products_page_{page}"
        
        cache_key = F"products:v{version}:{request.get_full_path()}"
        
        data = cache.get(cache_key)
        if data:
            print('cache hit')
            return Response(data)
        print('redis cache miss ')
        
        responce= super().list(request,*args,**kwargs)
        
        cache.set(cache_key,responce.data,timeout=60 * 5)
        
        return responce
    
class ProductDetailView(RetrieveAPIView):
    
    permission_classes =[AllowAny]
    serializer_class = ProductSerializer
    queryset=Product.objects.select_related('owner','category').all()
    
    
    def retrieve(self, request, *args, **kwargs):
        
        version = cache.get('product_version',1)
        
        product_id = kwargs.get('pk')
        
        cache_key = f"Product_detail v:{version}:{product_id}"
        
        data = cache.get(cache_key)
        
        if data:
            print('cache hit')
            return Response(data)
        
        print('cache mis db hit')
        
        responce = super().retrieve(request,*args,**kwargs)
        
        cache.set(cache_key,responce.data,timeout=60*10)
        
        return responce
        
  
    
# Product Owners

# class OwnerProductView(ModelViewSet):
#     serializer_class = ProductSerializer
#     pagination_class = CustomPagination

#     filter_backends=[DjangoFilterBackend,
#                      SearchFilter,
#                      OrderingFilter
                     
#                      ]
#     # filterset_fields= ['category_name','price_per_day','title']
#     filterset_class = ProductFilter
#     search_fields = ['title']
#     ordering_fields = ['price_per_day','brand_name']
#     ordering = ['brand_name']
 
#     def get_queryset(self):
#         return Product.objects.select_related('owner', 'category').filter(owner=self.request.user)
    
    
# Admin only 

class CategoryView(ListCreateAPIView):
    
    
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    pagination_class =None