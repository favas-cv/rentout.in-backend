from django.shortcuts import render
from .models import Cart,Wishlist
from accounts.models import User
from products.models import Product
from .serializers import  CartSerializer,WishlistSerializer

from rest_framework.generics import ListCreateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView,RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.generics import ListCreateAPIView


class CartApiView(APIView):
    
    def get(self,request):
        
        cart_items=Cart.objects.filter(user=self.request.user)
        serializer=CartSerializer(cart_items,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error':'the product is not avialibale '})
        

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, 
            product_id=product_id,
      
            defaults={'quantity': 1}
        )

        if not created:
            return Response({'error': 'Already in cart'})

        return Response({'msg': 'Added to cart'})
    

        
   
class CartProductDetailView(APIView):
    
    def get_object(self,request,pk):
        return Cart.objects.filter(id=pk,user=request.user).first()
    
    def patch(self,request,pk):

        cart_item = self.get_object(request,pk)
        if not cart_item:
            return Response({'error':'Not Found'})
        
        
        serializer=CartSerializer(cart_item,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        
        
    def delete(self, request,pk):

        cart_item = self.get_object(request,pk)
        

        if not cart_item:
            return Response(
                {"msg": "Item not found in your cart"},
                status=404
            )
        cart_item.delete()
        
        return Response(
            {"msg": "Item removed successfully"},
            status=200
        )
        
        
class CartIncreaseView(APIView):
    def get_object(self,request,pk):
        return Cart.objects.filter(id=pk,user=request.user).first()
    
    def post(self,request,pk):
        cart_item=self.get_object(request,pk)
        if not cart_item:
            return Response({'error':'the irtrem not found'})
        
        cart_item.quantity+=1
        cart_item.save()
        return Response({'quanitity':cart_item.quantity})
            
        
class CartDecreaseView(APIView):
    def get_object(self,request,pk):
        return Cart.objects.filter(id=pk,user=request.user).first()
    
    def post(self,request,pk):
        cart_item=self.get_object(request,pk)
        if not cart_item:
            return Response({'error':'the irtrem not found'})
        
        cart_item.quantity-=1
        if cart_item.quantity<=0:
            cart_item.delete()
            return Response({'msg':'the item was deleted'})
        cart_item.save()
        return Response({'quanitity':cart_item.quantity})
            

class ClearCartAPIView(APIView):

    def delete(self, request):
        user = request.user

        deleted_count, _ = Cart.objects.filter(user=user).delete()

        return Response(
            {
                "message": "Cart cleared successfully",
                "deleted_items": deleted_count
            },
            status=200
        )    
        
            
class WishlistApiView(APIView):

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"msg": "Product ID required"}, status=400)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product_id=product_id 
        )

        if not created:
            return Response({"msg": "Already in wishlist"})

        return Response({"msg": "Added to wishlist"})

    def delete(self, request):
        product_id = request.data.get("product_id")

        deleted, _ = Wishlist.objects.filter(
            user=request.user,
            product_id=product_id 
        ).delete()

        if deleted == 0:
            return Response({"msg": "Item not found"}, status=404)
        
        return Response({'msg':'the item was deleted '})
