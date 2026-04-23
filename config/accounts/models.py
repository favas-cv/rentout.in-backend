from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

from django.utils import timezone
import random

class User(AbstractUser):
    email=models.EmailField(unique=True)
    is_owner=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=True)
    kyc_status=models.CharField(default='verified')
    stage=models.CharField(default='basic')
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =['username']
    

# class Verification(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
    
#     document = models.ImageField()
#     selfie = models.ImageField()
    
#     status = models.CharField()


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
    
    

    
    
    