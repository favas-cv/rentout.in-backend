
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing  import websocket_urlpatterns
from .middleware import JWTAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({

    "http": get_asgi_application(),
    # ↑ all normal GET/POST requests still work as usual

    "websocket": JWTAuthMiddleware(
        # ↑ AuthMiddlewareStack reads the session cookie and puts the
        #   logged-in user into scope["user"] — so inside your consumer
        #   you can do self.scope["user"] to get the current user

        URLRouter(websocket_urlpatterns)
        # ↑ URLRouter maps ws:// URLs to the right consumer
        #   (same idea as urls.py but for WebSockets)
    ),
})



# application = get_asgi_application()
