from django.db import models
from accounts.models import User
from utils.models  import TimeStampedModel


class Category(TimeStampedModel):
    category=models.CharField(max_length=25,unique=True)

 
class Product(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,db_index=True)
    
    brand_name = models.CharField(max_length=25, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    material = models.CharField(max_length=25, null=True, blank=True)
    locality = models.CharField(max_length=30, null=True, blank=True,db_index=True)
    color=models.CharField(max_length=25,default='blue')
    age_years = models.IntegerField(null=True, blank=True)
    
    min_rental_days=models.IntegerField(default=15)
    price_per_day = models.BigIntegerField(null=True, blank=True)
    security_deposit = models.BigIntegerField(null=True, blank=True)
    monthly_rent = models.BigIntegerField(null=True, blank=True)
    offer_price = models.BigIntegerField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-price_per_day']
 
class ProductImage(models.Model):
    # FILE_TYPES = (
    # ("image", "Image"),
    # ("model", "3D Model"),
    # )
    
    
    product =models.ForeignKey(
         Product,
         on_delete=models.CASCADE,
         related_name='images'
     )
     
    image_url =models.URLField()
    model3d_url = models.URLField(null=True,blank=True)
      