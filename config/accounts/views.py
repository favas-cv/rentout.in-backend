from django.shortcuts import render

# Create your views here.
from .models import OTPVerification
from .serializers import (RegisterSerializer,LoginSerializer,
                          GoogleAuthSerializer,
                          ProfileSerializer
                          
                          
                          )

from rest_framework.response import Response
from rest_framework.views  import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_welcome_mail,logoutmail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

from rest_framework.parsers import MultiPartParser,FormParser
    



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
                samesite='Lax',
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
                
                'user':{
                    'id':user.id,
                    'username':user.username,
                    'email':user.email,
                    'is_staff':user.is_staff,
                    'is_live':user.is_live
                }
            },status=200)
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
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
                "user":user.username,
                "is_staff":user.is_staff
                
            },status=201)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )
            return response

        return Response(serializer.errors, status=400)
     
     
     
     
from rest_framework.permissions import AllowAny
class RefreshView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'Session expired please login again'},
                status=401
            )

        try:

            refresh = RefreshToken(refresh_token)

            new_access = str(refresh.access_token)

            # IMPORTANT
            new_refresh = str(refresh)

            response = Response({
                'access': new_access
            })

            # UPDATE COOKIE
            response.set_cookie(
                key='refresh_token',
                value=new_refresh,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )

            return response

        except Exception as e:
            print(e)

            return Response(
                {'error': str(e)},
                status=401
            )        
        


class LogoutView(APIView):

    permission_classes = [AllowAny]
    authentication_classes =[]

    def post(self, request):

        try:

            refresh_token = request.COOKIES.get('refresh_token')

            response = Response(
                {'msg': 'Logout successful'},
                status=200
            )

            if refresh_token:

                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()

                except Exception:
                    pass

            response.delete_cookie('refresh_token')

            return response

        except Exception:

            response = Response(
                {'msg': 'Logout successful'},
                status=200
            )

            response.delete_cookie('refresh_token')

            return response
        
        
        
        
        
class ProfileView(APIView):
    
    parser_classes =[MultiPartParser,FormParser]
    
    
    def get(self,request):
        
        user = request.user
        
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    
    def patch(self,request):
        user =request.user
        serializer = ProfileSerializer(user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg':'profile updated'})
        return Response(serializer.errors)
    
        