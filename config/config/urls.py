
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include('accounts.urls')),
    path('api/products/',include('products.urls')),
    path('api/cart/',include('cart.urls')),
    path('api/booking/',include('booking.urls')),
    path('api/room/',include('room.urls')),
    path('api/address/',include('address.urls')),
    path('api/owner/',include('ownerdashboard.urls')),
    path('api/kyc/',include('kyc.urls')),
    path('api/chatbot/',include('chatbot.urls')),
    path('api/chat/',include('chat.urls')),
    path('api/notifications/',include('notification.urls')),
    path('api/admin/',include('admindashboard.urls')),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='swagger-ui'),
]
