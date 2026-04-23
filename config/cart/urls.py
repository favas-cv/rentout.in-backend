from django.urls import path
from .views import (CartApiView,WishlistApiView,
                    CartProductDetailView,CartIncreaseView,
                    CartDecreaseView,ClearCartAPIView
)
urlpatterns = [
    path('',CartApiView.as_view()),
    path('clear/',ClearCartAPIView.as_view()),
    path('wishlist/',WishlistApiView.as_view()),
    # path('wishlist/remove/',WishlistDeleteView.as_view()),
    path('<int:pk>/',CartProductDetailView.as_view()),
    path('<int:pk>/increase/',CartIncreaseView.as_view()),
    path('<int:pk>/decrease/',CartDecreaseView.as_view()),
]
  