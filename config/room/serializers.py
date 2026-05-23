from rest_framework import serializers
from .models import Room,RoomProduct
from products.serializers import ProductSerializer

class RoomProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model =RoomProduct
        fields=['id','product']
        

        
class RoomSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    products = RoomProductSerializer(many=True,read_only =True)
    
    class Meta:
        model=Room
        fields='__all__'
        
        
class AddProductSerializer(serializers.Serializer):
    product =serializers.IntegerField()
   