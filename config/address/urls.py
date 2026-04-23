from django.urls import path
from .views import AddressView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',AddressView,basename='delivery-address')

urlpatterns = [
    
]+router.urls
