from django.shortcuts import render
from .serializers import ChatResponceSerializer,ChatRequestSerializer
from .rag_engine import ask
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import uuid
from .models import ChatMessage,ChatSession


class ChatApiView(APIView):
    
    permission_classes= [AllowAny]
    
    def post(self,request):
        serializer = ChatRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        
        user_message = serializer.validated_data['message']
        
        session_key = request.data.get('session_key') or str(uuid.uuid4())
        
        session,_ = ChatSession.objects.get_or_create(
            session_key=session_key,
            defaults={"user":request.user if request.user.is_authenticated else None}
        )
        
        ChatMessage.objects.create(
            session=session,
            role='user',
            message=user_message
            
        )
        
        
        result = ask(user_message)
        
        ChatMessage.objects.create(
            session=session,
            role='bot',
            message=result['answer']
        )
        
        return Response({
            "session_key": session_key,   # frontend saves this
            "answer": result["answer"],
            "matched_products": result.get("matched_products", [])
        },status=200)

class ChatHistory(APIView):
    permission_classes= [AllowAny]
    
    
    def get(self,request,session_key):
        try:
            session = ChatSession.objects.get(session_key=session_key)
            messages = session.messages.all()
            
            data =[
                {
                    'role':msg.role,
                    'message':msg.message,
                    'created_at':msg.created_at
                    
                }
             for msg in messages
            ]
            
            return Response(data,status=200)
            
        except ChatSession.DoesNotExist:
            return Response([],status=200)
            