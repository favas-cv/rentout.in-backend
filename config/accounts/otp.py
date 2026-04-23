
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import OTPVerification,User
from .serializers import SendOTPSerializer,VerifyOTPserializer
from utils.email import send_otp_email



import random
import secrets

def generate_otp():
    return str(random.randint(100000,999999))



def generate_reset_token():
    return secrets.token_urlsafe(32)

def generate_session_ref():
    return secrets.token_urlsafe(32)


class SendOTPView(APIView):
    
    permission_classes =[AllowAny]
    
    def post(self,request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            purpose = serializer.validated_data['purpose']
            
            if purpose == 'password_reset':
                if not User.objects.filter(email=email).exists():
                    return Response({'error':'the Use is not found , please register'})
                
            
            
            
            OTPVerification.objects.filter(email=email).delete()
            
            otp = generate_otp()
            session_ref = generate_session_ref()
            OTPVerification.objects.create(email=email,otp=otp,
                                           purpose=purpose,
                                           session_ref=session_ref
                                           )
            
            send_otp_email.delay(email,otp)
            
            return Response({'msg':'OTP sent to your email','session_ref':session_ref},status=200)
        return Response(serializer.errors,status=400)

  

class VerifyOTPVIew(APIView):
    
    permission_classes =[AllowAny]
    
    
    def post(self,request):
        
        serializer = VerifyOTPserializer(data=request.data)
        
        if serializer.is_valid():
            session_ref =serializer.validated_data['session_ref']
            otp=serializer.validated_data['otp']
            
            try:
                # record = OTPVerification.objects.filter(
                #     email=email,is_verified = False
                # ).latest('created_at')
                
                record  = OTPVerification.objects.filter(
                    session_ref=session_ref,is_verified = False
                ).latest('created_at')
                
            except OTPVerification.DoesNotExist:
                return Response({'error':'OTP not found'},status=400)
            
            if record.is_expired():
                return Response({'error':'OTP has expired'},status=400)
            
            if record.otp != otp:
                return Response({'error':'Invalid OTP'},status=400)
            
            record.is_verified = True
            response_data = {'msg':'OTp verified'}
            
            if record.purpose == 'password_reset':
                reset_token = generate_reset_token()
                record.reset_token = reset_token
                response_data['reset_token'] = reset_token
                
            record.save()
            return Response(response_data,status=200)
            
            
            
            # return Response({'msg':'Email verification successfull'},status=200)
        return Response(serializer.errors,status=200)
