from .views import CategoryView,ProductView,ProductDetailView #OwnerProductView,
from django.urls import path

# from rest_framework.routers import DefaultRouter

# router=DefaultRouter()
# router.register('owner',OwnerProductView,basename='owner-products')

urlpatterns = [
    path('category/',CategoryView.as_view()),
    path('',ProductView.as_view()),
    path('<int:pk>/',ProductDetailView.as_view()),
    
]
# +router.urls
  