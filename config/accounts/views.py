from django.shortcuts import render

# Create your views here.
from .models import OTPVerification
from .serializers import (RegisterSerializer,LoginSerializer,
                          GoogleAuthSerializer,UserProfileSerializer,
                          
                          
                          )

from rest_framework.response import Response
from rest_framework.views  import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_welcome_mail,logoutmail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
    



class RegisterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self,request):
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            verified = OTPVerification.objects.filter(
                email=email,is_verified=True
            ).exists()
            
            if not verified:
                return Response({'error':'Email is not verified.Please verify OTP first'},status=400)
            
            
            user = serializer.save()
            
            OTPVerification.objects.filter(email=email).delete()
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token =str(refresh)
            
            send_welcome_mail.delay(user.email)
            
            response = Response({
                'access':access_token,
                'user':user.email,
                'msg':'Use is registred and logged in'
            },
                                status=201)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            
            return response
        
        return Response(serializer.errors,status=400)
    
class LoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token =str(refresh)
            response = Response({
                'access':access_token,
                
                'user':user.email
            },status=200)
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            return response
            
            
        return Response(serializer.errors,status=400)
        


class GoogleLoginView(APIView):
    permission_classes =[AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)
            access_token =str(refresh.access_token)
            refresh_token=str(refresh)
            

            response= Response({
                "access": access_token,
                "user":user.username
                
            },status=201)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            return response

        return Response(serializer.errors, status=400)
     
     
     
     
     
class RefreshView(APIView):
    
    def post(self,request):
        refresh_token=request.COOKIES.get('refresh_token')
        print(refresh_token)
        
        if not refresh_token:
            return Response(
                {'error':'session expired please log again'}
            ,status=401)
        refresh =RefreshToken(refresh_token)
        new_access=str(refresh.access_token)
        return Response({'access':new_access})
    
class LogoutView(APIView):
    def post(self,request):
        try:
            user_email = request.user.email if request.user.is_authenticated else None
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                respose = Response({'msg':'logout sucessful'})
                respose.delete_cookie('refresh_token')
                if user_email:
                    
                    logoutmail.delay(request.user.email)
                return respose
            return Response({'error':'you are not logged'})
        except Exception as e:
            return Response({'error':str(e)},status=400)

class ManageProfileView(APIView):
    
    def get(self,request):
        
        
        user =request.user
        
        serializer = UserProfileSerializer(user)
        
        return Response(serializer.data)