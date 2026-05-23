from django.db import models
from accounts.models import User



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("ORDER", "ORDER"),
        ("BOOKING_STATUS_UPDATE", "BOOKING_STATUS_UPDATE"),
        ("DEPOSIT_STATUS_UPDATE", "DEPOSIT_STATUS_UPDATE"),
        # ("PAYMENT", "PAYMENT"),
        ("MESSAGE", "MESSAGE"),
        ("AD", "AD"),
        ("OFFERS", "OFFERS"),
        ("NEW_BOOKING", "NEW_BOOKING"),
        ("CANCELLED", "CANCELLED"),
    )
    
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='sent_notifications'
    )
    
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    
    notification_type = models.CharField(max_length=50,
                                         choices=NOTIFICATION_TYPES
                                         )
    title = models.CharField(max_length=255)
    
    message=models.TextField()
    
    redirect_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['-created_at']
        
        
        
class UserFCMToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    token = models.TextField(unique=True)
    
    created_at=models.DateTimeField(auto_now_add=True)