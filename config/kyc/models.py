from django.db import models

# Create your models here.
from accounts.models import User
from utils.models import TimeStampedModel


class KycDocs(TimeStampedModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='documents')
    document1 = models.URLField()
    document2=models.URLField()
    selfie = models.URLField()
    
    status = models.CharField(default='pending')
      
 