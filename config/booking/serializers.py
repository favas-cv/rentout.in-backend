from .models import Booked_items,Booking
from products.models import Product

from rest_framework import serializers
from accounts.serializers import UserSerializer
from accounts.models import User





class BookedUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =User
        fields =['username','email']






class BookedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booked_items 
        fields='__all__'
        
        
         
class BookingSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    user_details = BookedUserSerializer(
        source='user',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'

    def get_items(self, obj):

        active_items = obj.items.exclude(
            status__in=['CANCELLED', 'RETURNED']
        )

        return BookedItemsSerializer(
            active_items,
            many=True
        ).data
        
