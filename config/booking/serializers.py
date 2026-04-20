from .models import Booked_items,Booking


from rest_framework import serializers

class BookedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booked_items 
        fields='__all__'
        
        
         
class BookingSerializer(serializers.ModelSerializer):
    
    items =BookedItemsSerializer(many=True,read_only=True)
    
    class Meta:
        model=Booking
        fields='__all__'
        

        
 
