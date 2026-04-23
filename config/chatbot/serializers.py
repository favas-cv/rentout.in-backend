from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
    
class ChatResponceSerializer(serializers.Serializer):
    answer = serializers.CharField()
    
    
