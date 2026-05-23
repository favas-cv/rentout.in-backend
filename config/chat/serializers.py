from rest_framework import serializers
from .models import ChatRequest,Message
from accounts.serializers import UserSerializer
from accounts.models import User


class ChatRequestSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver_details = UserSerializer(source='receiver', read_only=True)
    
    
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sender_details = UserSerializer(source='sender', read_only=True)
    class Meta:
        model = ChatRequest
        fields = [
            'id',
            'room',
            'sender',
            'sender_details',
            'receiver',          # for POST
            'receiver_details',  # for GET
            'status',
            'created_at'
        ]
        read_only_fields = ['sender']

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =Message
        fields='__all__'