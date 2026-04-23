from django.db import models

from accounts.models import User


class ChatSession(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='chat_sessions',null=True,blank=True)
    
    session_key = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"session {self.session_key} - {self.user or 'Guest'}"
    
class ChatMessage(models.Model):
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    message = models.TextField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['created_at']
        
    def __str__(self):
        return f"{self.role} : {self.message[:50]}"
    
