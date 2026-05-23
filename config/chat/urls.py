from django.urls import path
from .views import update_chat_request,SendChatRequest,MyChatRequests,MessagesHistoryView

urlpatterns = [
    path('send-request/',SendChatRequest.as_view()),
    path('my-requests/',MyChatRequests.as_view()),
    path("update-request/<int:request_id>/",update_chat_request, name="create_room"),
    path('my-history/<int:room_id>/',MessagesHistoryView.as_view()),
]