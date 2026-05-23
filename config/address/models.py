from django.db import models
from accounts.models import User
from utils.models import TimeStampedModel

class Address(TimeStampedModel):
    
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    house_name=models.CharField(max_length=233,null=True,blank=True)
    street = models.CharField(max_length=255,null=True,blank=True)
    landmark=models.CharField(max_length=255,blank=True,null=True)
    
    city=models.CharField(max_length=155)
    
    district = models.CharField(max_length=155)
    state = models.CharField(max_length=155,blank=True,null=True)
    country=models.CharField(max_length=155)
    
    zipcode=models.CharField(max_length=10,blank=True,null=True)
    
    phone = models.CharField(max_length=12,blank=True,null=True)
    is_default =models.BooleanField(default=True)
    
 
    
    
    
     