from django.db import models
from products.models import Product
from accounts.models import User
from room.models import Room
from utils.models import TimeStampedModel
    
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    class Meta:
        unique_together=('user','product')
        
        
class Cart(TimeStampedModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    # start_date=models.DateField(null=True,blank=True)
    # end_date=models.DateField(null=True,blank=True)
    # room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        unique_together=('user','product')
        ordering=['created_at']
        
        

   