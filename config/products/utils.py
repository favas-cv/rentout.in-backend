from django.core.cache import cache
from .models import Product
import django_filters

def invalidate_product_cache():
    version = cache.get("product_version", 1)
    cache.set("product_version", version + 1)
    
    


class ProductFilter(django_filters.FilterSet):

    # 🔍 category by name
    category = django_filters.CharFilter(
        field_name='category__category',
        lookup_expr='icontains'
    )

    # 🔍 brand filter
    brand = django_filters.CharFilter(
        field_name='brand_name',
        lookup_expr='icontains'
    )
    
    location = django_filters.CharFilter(
        field_name='locality',
        lookup_expr='icontains'
    )
    
    color = django_filters.CharFilter(
        field_name='color',
        lookup_expr='icontains'
    )
    
    

    # 🔍 price range
    min_price = django_filters.NumberFilter(
        field_name='price_per_day',
        lookup_expr='gte'
    )

    max_price = django_filters.NumberFilter(
        field_name='price_per_day',
        lookup_expr='lte'
    )

    class Meta:
        model = Product
        fields = ['category', 'brand_name']