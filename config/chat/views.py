from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom,ChatRequest,Message
from accounts.models import User
from rest_framework.views import APIView
from .serializers import ChatRequestSerializer,MessageSerializer
from django.db.models import Q
from rest_framework.generics import ListAPIView
from accounts.permissions import IsActiveUsers


class SendChatRequest(APIView):

    permission_classes =[IsActiveUsers]

    def post(self, request):

        serializer = ChatRequestSerializer(
            data=request.data,
            context={'request': request}   # ✅ REQUIRED
        )

        if serializer.is_valid():
            receiver = serializer.validated_data['receiver']

            if ChatRequest.objects.filter(
                sender=request.user,
                receiver=receiver
            ).exists():
                return Response({'error': 'request already sent'}, status=400)

            serializer.save()   # ✅ sender auto-set
            return Response({'msg': 'request sent'}, status=201)

        return Response(serializer.errors)

class MyChatRequests(APIView):
    permission_classes =[IsActiveUsers]
    
    def get(self,request):
        
        queryset = ChatRequest.objects.filter(Q(sender = request.user) | Q(receiver = request.user))
        serializer = ChatRequestSerializer(queryset,many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsActiveUsers])
def update_chat_request(request, request_id):
    
    chat_request = get_object_or_404(ChatRequest,id=request_id)
    
    if chat_request.receiver != request.user:
        return Response({'error':'Not Allowed you are sender and receiver'})
    
    status_value = request.data.get('status')
    
    if status_value not in ['accepted','rejected']:
        return Response({'error':'Invalid status'})
    
    
    if chat_request.status == 'accepted' and chat_request.room:
     
        return Response({
            "room_id": chat_request.room.id,
            "message":"already connected"
        })
    
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
        
    chat_request.room = room
    chat_request.save()

    return Response({
        "room_id": room.id,
        "message":"chat started"
    })
     

from .pagination import ChatPagination
class MessagesHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = MessageSerializer
    pagination_class =ChatPagination

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')   # ✅ correct

        room = get_object_or_404(ChatRoom, id=room_id)

        # 🔒 SECURITY CHECK
        if not room.participants.filter(id=self.request.user.id).exists():
            return Message.objects.none()

        return Message.objects.filter(room=room).order_by('-timestamp')
    
     