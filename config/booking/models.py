from django.db import models
from accounts.models import User
from products.models import Product
from address.models import Address
from utils.models import TimeStampedModel

class Reservation(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)#,null=True,blank=True) #chnage nul and black in prdutin
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.IntegerField()
    expires_at = models.DateTimeField()
    
    total_rent = models.FloatField(default=0)
    total_deposit =models.FloatField(default=0)
    # tax_amount = models.FloatField(default=0)
    # delivery_package_charge = models.FloatField(default=0)
    # convenience_charge = models.FloatField(default=0)
    
    # total_paid = models.FloatField(default= 0)
    
    razorpay_order_id = models.CharField()
    
    is_paid =models.BooleanField(default=False)
    
     



class Booking(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    address_snapshot = models.JSONField()
    
    total_rent_money=models.FloatField(default=0)
    total_deposit_money=models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    delivery_package_charge = models.FloatField(default=0)
    convenience_charge = models.FloatField(default=0)
    total_paid = models.FloatField(default= 0)
    
    payment_id = models.CharField(max_length=255, null=True,blank=True)
    
    # status=models.CharField(default='PENDING',choices=[
    #     ('PENDING', 'Pending'),
    #     ('CONFIRMED', 'Confirmed'),
    #     ('SHIPPED', 'Shipped'),
    #     ('DELIVERED', 'Delivered'),
    #     ('RETURNED', 'Returned'),
    #     ('CANCELLED', 'Cancelled'),
    # ])
    # deposit_status=models.CharField(default='PENDING')
     
     
class Booked_items(TimeStampedModel):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    product_snapshot = models.JSONField()
    
    start_date=models.DateField()
    end_date=models.DateField() 
     

    quantity=models.IntegerField() 
    
    status=models.CharField(default='PENDING',choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('CANCELLED', 'Cancelled'),
    ])
    deposit_status=models.CharField(default='PENDING')
    
    
    
    
     