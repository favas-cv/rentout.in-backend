from .views import AddProductToRoomView,RoomManageView,RemoveProductFromRoomView
from django.urls import path
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register('',RoomManageView,basename='room-manage')


urlpatterns = [
    path('add-product/<int:pk>/',AddProductToRoomView.as_view()),
    path('product/<int:pk>/remove/',RemoveProductFromRoomView.as_view()),
]+router.urls
  