from django.shortcuts import render

# Create your views here.
from .models import Room,RoomProduct
from .serializers import RoomSerializer,RoomProductSerializer,AddProductSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from accounts.permissions import IsActiveUsers

# class RoomListView(ListCreateAPIView):
#     serializer_class = RoomSerializer
    
class RoomManageView(ModelViewSet):
    permission_classes =[IsActiveUsers]
    
    def get_queryset(self):
        return Room.objects.filter(user=self.request.user)
    
    serializer_class=RoomSerializer
    
     
class AddProductToRoomView(APIView):
    permission_classes = [IsActiveUsers]
    
    @swagger_auto_schema(request_body=AddProductSerializer)
    def post(self,request,pk):
        
        room = Room.objects.filter(id=pk).first()
        if not room:
            return Response({'error':'the Room not found'})
        
        product_id = request.data.get('product')
        if not product_id:
            return Response({'error':'product not found'})
        
        #in here allowing dublicate bcz same products have so many times 
        
        RoomProduct.objects.create(
            room=room,
            product_id=product_id
        )
        
        return Response({'msg':'the product added '})
    
class RemoveProductFromRoomView(APIView):
    
    permission_classes = [IsActiveUsers]
    
    
    def delete(self,request,pk):
        # room_p_id = request.data.get('room_product')
        
        room_product = RoomProduct.objects.filter(
            id=pk
        ).first()
        
        if not room_product:
            return Response({'error':'Product not found'})
        
        room_product.delete()
        
        return Response({
            'msg':'Product removed Successfully'
        })
    
        
    