from rest_framework import serializers
from .models import Product,Category,ProductImage
from accounts.serializers import UserSerializer
import cloudinary.uploader


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta: 
        model=Category
        fields=['category']
    
    
    
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields =['product','image_url']

 


class ProductSerializer(serializers.ModelSerializer):
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    
    
    product_image =ProductImageSerializer(
        many=True,
        read_only=True,
        source='images'
    )

    category=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    
    # category_details = CategorySerializer(source='category', read_only=True)
    owner_details = UserSerializer(source='owner', read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model=Product
        fields='__all__'
        
    
    def create(self,validated_data):
        image_files=validated_data.pop('images',[])
        product = Product.objects.create(**validated_data)
        
        for image in image_files:
            upload=cloudinary.uploader.upload(
                image,
                folder='rentoutProducts'
            )
            
            ProductImage.objects.create(
                product=product,
                image_url=upload.get('secure_url')
            )
        return product
    
        
    def validate_title(self,value):
        if len(value) < 3:
            raise serializers.ValidationError('The name must be 3 character')
        return value
    