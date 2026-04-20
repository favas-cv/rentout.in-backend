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

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'quantity']
        
    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError('the quantity must be 1 or more')
        
        
        
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    # product_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(),
    #     source='product',
    #     write_only=True
    # )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id']
        
    
        
        
        
