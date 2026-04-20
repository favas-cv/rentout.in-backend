from django.urls import path
from .views import AddressView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('address',AddressView,basename='delivery-address')

urlpatterns = [
    
]+router.urls
