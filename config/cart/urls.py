from django.urls import path
from .views import CartApiView,WishlistApiView,CartProductDetailView,CartIncreaseView,CartDecreaseView

urlpatterns = [
    path('cart/',CartApiView.as_view()),
    # path('cart/remove/',CartDeleteView.as_view()),
    path('wishlist/',WishlistApiView.as_view()),
    # path('wishlist/remove/',WishlistDeleteView.as_view()),
    path('cart/<int:pk>/',CartProductDetailView.as_view()),
    path('cart/<int:pk>/increase/',CartIncreaseView.as_view()),
    path('cart/<int:pk>/decrease/',CartDecreaseView.as_view()),
]
  