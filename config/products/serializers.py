from rest_framework import serializers
from .models import Product,Category,ProductImage
from accounts.serializers import UserSerializer
import cloudinary.uploader


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta: 
        model=Category
        fields=['id','category']
    
    
    
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:  
        model=ProductImage
        fields =['product','image_url','model3d_url']

 


class ProductSerializer(serializers.ModelSerializer):
    
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    model_3d= serializers.FileField(
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
    
    category_name = serializers.CharField(
        source='category.category',
        read_only=True
    ) 

    owner_details = UserSerializer(source='owner', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id',read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model=Product
        fields='__all__'
        
    
    def create(self,validated_data):
        image_files=validated_data.pop('images',[])
        model_3d = validated_data.pop('model_3d',None)
        
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
        
        if model_3d:
            model_upload = cloudinary.uploader.upload(
                model_3d,
                resource_type='raw',
                folder ='rentout3Dmodels'
            )
            
            ProductImage.objects.create(
                product=product,
                model3d_url = model_upload.get(
                    'secure_url'
                )
            )
        
        # invalidate_product_cache()
        return product
    
    def update(self, instance, validated_data):

        image_files = validated_data.pop(
            'images',
            []
        )

        model_3d = validated_data.pop(
            'model_3d',
            None
        )

        # update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # upload new images
        for image in image_files:

            upload = cloudinary.uploader.upload(
                image,
                folder='rentoutProducts'
            )

            ProductImage.objects.create(
                product=instance,
                image_url=upload.get('secure_url')
            )

        # upload new 3d model
        if model_3d:

            model_upload = cloudinary.uploader.upload(
                model_3d,
                resource_type='raw',
                folder='rentout3Dmodels'
            )

            ProductImage.objects.create(
                product=instance,
                model3d_url=model_upload.get(
                    'secure_url'
                )
            )

        # invalidate_product_cache()
        return instance
    
        
    def validate_title(self,value):
        if len(value) < 3:
            raise serializers.ValidationError('The name must be 3 character')
        return value
    