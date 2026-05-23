from .models import Cart,Wishlist
from accounts.serializers import UserSerializer
from products.serializers import ProductSerializer
from rest_framework import serializers
from rest_framework.views  import APIView
from rest_framework.response import Response
from products.models import Product





class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    available = serializers.SerializerMethodField()
    unavailable_reason = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'quantity','available','unavailable_reason']
        
    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError('the quantity must be 1 or more')
        
    def get_available(self,obj):
        
        return (
            obj.product.is_active and
            obj.product.owner.is_live
        )
        
    def get_unavailable_reason(self,obj):
        
        if not obj.product.is_active:
            return "Product unavailable"
        
        if not obj.product.owner.is_live:
            return "owner unavailble now "
        
        return None
        
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    # product_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(),
    #     source='product',
    #     write_only=True
    # )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    available = serializers.SerializerMethodField()
    unavailable_reason = serializers.SerializerMethodField()
    

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id','available','unavailable_reason']
        
    
    def get_available(self,obj):
        
        return (
            obj.product.is_active and 
            obj.product.owner.is_live
        )
        
    def get_unavailable_reason(self,obj):
        
        if not  obj.product.is_active:
            return "Product is Unavailable"
        
        if not obj.product.owner.is_live:
            return "Owner is Unavailable"
        
        return None
        
