from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True,min_length=8)
    password2 =serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields =['email','password','password2']
        extra_kwargs ={
            'username':{'required':False}
        }
        
    def validate_password(self,value):
        
        if len(value) < 8:
            raise serializers.ValidationError({'error':'The password must be 8'})
        return value
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error':'password is mismatch '})
        return data

    def create(self,validated_data):
        validated_data.pop('password2')
        
        email = validated_data.get('email')
        
        username = email.split('@')[0]
        
        validated_data['username'] = username
        
        
        return User.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password =serializers.CharField(write_only=True)
    
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError({'error':'password must be min 8 '})
        return value
    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        
        user_obj = User.objects.filter(email=email).first()
        
        # if user_obj and not user_obj.is_live:
        #     raise serializers.ValidationError({
        #         'error':'Your account has been blocked. please contact support care'
        #     })
            
        
        user= authenticate(username=email,password=password)
        
        if not  user:
            raise  serializers.ValidationError({'error':'invalid email or password'})
        data['user']=user
        return data 
    


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get("token")

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
 
            email = idinfo.get("email")
            name = idinfo.get("name")

            if not email:
                raise serializers.ValidationError("Email not found")

        except Exception:
            raise serializers.ValidationError("Invalid Google token")

        
            
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                'is_active':True,
            }
        )
        
        if created:
            user.set_unusable_password()
            user.save()
        

        return {"user": user}
    
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ['email','is_owner','is_verified','stage']
        
        
class SendOTPSerializer(serializers.Serializer):
    email=serializers.EmailField()
    purpose = serializers.ChoiceField(choices=['signup','password_reset'])
    
class VerifyOTPserializer(serializers.Serializer):
    # email=serializers.EmailField()
    session_ref = serializers.CharField()
    otp = serializers.CharField(max_length =6,min_length = 6)
    # purpose = serializers.ChoiceField(choices=['signup','password_reset'])
    
class PasswordResetSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    password1 =serializers.CharField(min_length=8)
    password2 =serializers.CharField(min_length=8)
    
    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'error':'password is mismatch '})
        return data
   

    
class ProfileSerializer(serializers.ModelSerializer):
    
    profile_pic_url = serializers.SerializerMethodField()

    class Meta:
        model= User
        fields =['id','first_name','last_name',
                 
                 'email','is_owner','is_verified','stage',
                 'profile_pic','profile_pic_url',
                 
                 
                 ]
        
        extra_kwargs ={
            'email':{'read_only':True},
            'is_owner':{'read_only':True},
            'is_verified':{'read_only':True},
            'stage':{'read_only':True},
            'profile_pic':{'write_only':True}
            
        }
        
        
    def get_profile_pic_url(self,obj):
        if  obj.profile_pic:
            return obj.profile_pic.url
        return None
        
        
    
    
