from django.urls import re_path
from .consumers  import ChatConsumer

# These are the ws:// URLs your frontend will connect to
# re_path is used because WebSocket URLs can have dynamic segments like room IDs

websocket_urlpatterns = [

    # ws://localhost:8000/ws/chat/42/
    #                              ↑ room_id — captured and passed to consumer
    re_path(
        r"ws/chat/(?P<room_id>\d+)/$",
        ChatConsumer.as_asgi()
        # .as_asgi() is like .as_view() for class-based views
        # it wraps the consumer so Channels knows how to call it
    ),
] 