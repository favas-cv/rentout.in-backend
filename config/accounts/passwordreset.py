from rest_framework.views import APIView
from .models import OTPVerification
from .serializers import PasswordResetSerializer
from rest_framework.response import Response
from accounts.models import User
from rest_framework.permissions import AllowAny

class PasswordResetView(APIView):
    
    permission_classes =[AllowAny]
    
    def post(self,request):
        
        
        
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            reset_token = serializer.validated_data['reset_token']
            new_password = serializer.validated_data['password1']
            
            try:
                record = OTPVerification.objects.get(
                    reset_token=reset_token,
                    purpose='password_reset',
                    is_verified = True
                )
            except OTPVerification.DoesNotExist:
                return Response({'error':'Invalid or Expired rest token.'},status=400)
            
            if record.is_expired():
                record.delete()
                return Response({'error':'Reset session expired'},status=400)
            
            user=User.objects.get(email=record.email)
            user.set_password(new_password)
            user.save()
            
            record.delete()
            
            return Response({'msg':'Password reset successfull'},status=200)
        return Response(serializer.errors,status=400)
                
        
            
            
        
        
    
        
            
        