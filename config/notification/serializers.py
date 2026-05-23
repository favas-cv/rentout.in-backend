from rest_framework import serializers
from .models import Notification,UserFCMToken

class UserFCMTokenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserFCMToken,
        fields  = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =Notification
        fields ='__all__'