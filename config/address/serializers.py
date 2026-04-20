from .models import Address

from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    
    class Meta:
        model=Address
        fields ='__all__'
    