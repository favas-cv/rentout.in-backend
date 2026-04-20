from .views import LoginView,RegisterView,GoogleLoginView,LogoutView,RefreshView
from django.urls import path

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('google/',GoogleLoginView.as_view()),
    path('refresh/',RefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
]
