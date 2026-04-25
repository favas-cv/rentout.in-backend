from rest_framework import serializers
from .models import ChatRequest


class ChatRequestSerializer(serializers.ModelSerializer):
    
    # sender = serializers.HiddenField(serializers.CurrentUserDefault())
    
    class Meta:
        model = ChatRequest
        fields =['id','receiver','status','created_at']