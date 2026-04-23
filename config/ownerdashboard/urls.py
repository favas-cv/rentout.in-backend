from django.urls import path
from .views import OwnerProductView,OwnerOrdersListView,OwnerDashboardStatsView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('products',OwnerProductView,basename='owner-products')
router.register('orders',OwnerOrdersListView , basename='owner-orders')

urlpatterns = [
    path('dashboard/',OwnerDashboardStatsView.as_view()),
]+router.urls

