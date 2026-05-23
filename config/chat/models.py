from django.db import models
from accounts.models import User

class ChatRoom(models.Model):
    
    participants = models.ManyToManyField(User,related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Room {self.id}"

class ChatRequest(models.Model):
    
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_requests')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_requests')
    status = models.CharField(
        max_length=20,choices=[('pending','Pending'),
                               ('accepted','Accepted'),
                               ('rejected','Rejected')
                       
                               ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,null=True,blank=True)

    
    
    
    
class Message(models.Model):
    
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,related_name='messages'
    )
    
    
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    is_read = models.BooleanField(default=False)
    
    read_at = models.DateTimeField(null=True,blank=True)
    is_delivered = models.BooleanField(default=False)
    
    # class Meta:
    #     ordering = ['timestamp']
         
    def __str__(self):
        return f"{self.sender.username} :{ self.content[:40]}"
