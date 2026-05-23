from django.db import models
from products.models import Product
from accounts.models import  User
from utils.models import TimeStampedModel



class Room(TimeStampedModel):
    
    title = models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # product=models.ForeignKey(Product,on_delete=models.CASCADE)
    

    
     
class RoomProduct(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='products')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)  