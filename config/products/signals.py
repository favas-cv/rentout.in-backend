from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .utils import invalidate_product_cache  # or import from views

@receiver(post_save, sender=Product)
def product_saved(sender, **kwargs):
    invalidate_product_cache()

@receiver(post_delete, sender=Product)
def product_deleted(sender, **kwargs):
    invalidate_product_cache()