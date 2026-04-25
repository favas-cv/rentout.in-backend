from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom,ChatRequest
from accounts.models import User
from rest_framework.views import APIView
from .serializers import ChatRequestSerializer
from django.db.models import Q


class SendChatRequest(APIView):
    
    def post(self,request):
        
        serializer = ChatRequestSerializer(data =request.data)
        
        if serializer.is_valid():
            
            receiver = serializer.validated_data['receiver']
            if ChatRequest.objects.filter(
                sender = request.user,
                receiver = receiver,
                status ='pending'
            ).exists():
                return Response({'error':'the request already sented'})
            
            serializer.save(sender=request.user)
            return Response({'msg':'request was sented'})
        return Response(serializer.errors)

class MyChatRequests(APIView):
    
    def get(self,request):
        
        queryset = ChatRequest.objects.filter(Q(sender = request.user) | Q(receiver = request.user))
        serializer = ChatRequestSerializer(queryset,many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_chat_request(request, request_id):
    
    chat_request = get_object_or_404(ChatRequest,id=request_id)
    
    if chat_request.receiver != request.user:
        return Response({'error':'Not Allowed you are sender and receiver'})
    
    status_value = request.data.get('status')
    
    if status_value not in ['accepted','rejected']:
        return Response({'error':'Invalid status'})
    
    
    if chat_request.status == 'accepted':
        return Response({'msg':'already connected'})
    
    chat_request.status =  status_value
    chat_request.save()
    
    
    if status_value =='rejected':
        return Response('Request rejected')
    
    
  
    room = ChatRoom.objects.filter(
        participants=chat_request.sender
    ).filter(
        participants=chat_request.receiver
    ).first()

    # create if not exists
    if not room :
        room = ChatRoom.objects.create()
        room.participants.add(chat_request.sender, chat_request.receiver)

    return Response({
        "room_id": room.id,
        "message":"chat started"
    })