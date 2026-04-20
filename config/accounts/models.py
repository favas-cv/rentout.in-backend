from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

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