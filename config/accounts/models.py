from django.db import models


from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    email=models.EmailField(unique=True)
    is_owner=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    kyc_status=models.CharField(default='PENDING')
    stage=models.CharField(default='basic')
    profile_pic = CloudinaryField('profile_pic',folder='rentout/profile_pics',blank=True,null=True)
    
    is_live = models.BooleanField(default=True)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =['username']
   
   



class OTPVerification(models.Model):
    
    PURPOSE=[
        ('signup','Signup'),
        ('password_reset','Password Reset')
    ]
    
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    purpose =models.CharField(max_length=20,choices=PURPOSE)
    session_ref=models.CharField(max_length=64,unique=True,blank=True,null=True)
    reset_token = models.CharField(max_length=64,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
    def __str__(self):
        return f"{self.email } - {self.purpose}"
     
    

    
    
    