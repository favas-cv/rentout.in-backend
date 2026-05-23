from django.shortcuts import render
from kyc.serializers import KycSerializer
from .serializers import KYCStatusUpdateSerializer
from kyc.models import KycDocs

from rest_framework.generics import ListAPIView

from .permissions import IsKYCAdmin

from accounts.models import User
from .serializers import AdminUserSerializer
from rest_framework.views import APIView
# from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from .serializers import AdminProductSerializer

 
# KYC SETUP



class AdminKYCListView(ListAPIView):

    serializer_class = KycSerializer

    # permission_classes = [IsAdminUser]
    permission_classes = [IsKYCAdmin]

    queryset = KycDocs.objects.select_related('user').all()
     
     

class UpdateKYCStatusView(APIView):

    # permission_classes = [IsAdminUser]
    permission_classes = [IsKYCAdmin]

    def patch(self, request, pk):

        try:

            kyc = KycDocs.objects.get(id=pk)

        except KycDocs.DoesNotExist:

            return Response(
                {'error': 'KYC not found'},
                status=404
            )

        serializer = KYCStatusUpdateSerializer(
            kyc,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )







# PRODUCTS SETUP
from products.utils import invalidate_product_cache

class AdminProductsListView(ListAPIView):
    
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes =[IsKYCAdmin]



class UpdateProductstatusView(APIView):
    
    permission_classes =[IsKYCAdmin]
    
    def patch(self, request, pk):

        try:

            product = Product.objects.get(id=pk)

        except Product.DoesNotExist:

            return Response(
                {'error': 'product not found'},
                status=404
            )

        serializer = AdminProductSerializer(
            product,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save()
            
            invalidate_product_cache()

            return Response(
                serializer.data,
                status=200
            )

        return Response(
            serializer.errors,
            status=400
        )



# OWNERS SETUP



class AdminUsersListView(ListAPIView):
    
    queryset =  User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes =[IsKYCAdmin]
    
class UpdateUserActiveView(APIView):
    
    permission_classes = [IsKYCAdmin]
    
    def patch(self,request,pk):
        
        try:
           user = User.objects.get(id=pk)
        
        except User.DoesNotExist:
            return Response({
                "error":"The user not found"
            })
            
        serializer = AdminUserSerializer(
            user,
            data=request.data,
            partial =True,
            context ={'request':request}
        )
        
        if serializer.is_valid():
            serializer.save()
            invalidate_product_cache()
            return Response(serializer.data,status=200)
        
        return Response(serializer.errors,status=400)
    