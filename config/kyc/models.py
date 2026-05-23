from django.db import models

# Create your models here.
from accounts.models import User
from utils.models import TimeStampedModel


class KycDocs(TimeStampedModel):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
        ('REVIEW', 'Review'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document1 = models.URLField()

    document2 = models.URLField()

    selfie = models.URLField()

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    #helper method
    
    def approve(self):

        self.status = 'VERIFIED'
        self.save()

        self.user.is_verified = True
        self.user.is_owner = True
        self.user.kyc_status = 'VERIFIED'
        self.user.save()


    def reject(self):

        self.status = 'REJECTED'
        self.save()

        self.user.is_verified = False
        self.user.is_owner = False
        self.user.kyc_status = 'REJECTED'
        self.user.save()
        
    def review(self):

        self.status = 'REVIEW'
        self.save()

        self.user.is_verified = False
        self.user.is_owner = False
        self.user.kyc_status = 'REVIEW'
        self.user.save()
