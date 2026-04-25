from .views import (LoginView,RegisterView,
                    GoogleLoginView,LogoutView,
                    RefreshView,
                    ProfileView
                    
                    )
from .otp import VerifyOTPVIew,SendOTPView
from .passwordreset import PasswordResetView
from django.urls import path

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('send-otp/',SendOTPView.as_view()),
    path('verify-otp/',VerifyOTPVIew.as_view()),
    path('password-reset/',PasswordResetView.as_view()),
    path('google/',GoogleLoginView.as_view()),
    path('refresh/',RefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('me/',ProfileView.as_view()),
]
