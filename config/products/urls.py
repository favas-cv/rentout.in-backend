from .views import CategoryView,ProductView,OwnerProductView,ProductDetailView
from django.urls import path

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('owner',OwnerProductView,basename='owner-products')

urlpatterns = [
    path('category/',CategoryView.as_view()),
    path('products/',ProductView.as_view()),
    path('product/<int:pk>/',ProductDetailView.as_view()),
    
]+router.urls
  