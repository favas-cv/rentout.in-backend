from django.db import models
from accounts.models import User
from products.models import Product
from address.models import Address
from utils.models import TimeStampedModel

class Reservation(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.IntegerField()
    expires_at = models.DateTimeField()
    
    total_rent = models.FloatField(default=0)
    total_deposit =models.FloatField(default=0)
    
    razorpay_order_id = models.CharField()
    
    is_paid =models.BooleanField(default=False)
    
    



class Booking(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total_rent_money=models.FloatField(default=0)
    total_deposit_money=models.FloatField(default=0)
    total_paid = models.FloatField(default= 0)
    
    payment_id = models.CharField(max_length=255, null=True,blank=True)
    
    status=models.CharField(default='pending')
    deposit_status=models.CharField(default='pending')
     
     
class Booked_items(TimeStampedModel):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    
    start_date=models.DateField()
    end_date=models.DateField() 
     
    booked_time_price=models.IntegerField()
    booked_time_deposit=models.IntegerField()
    quantity=models.IntegerField()
    
    
     