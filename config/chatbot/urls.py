from .views import ChatApiView,ChatHistory
from django.urls import  path


urlpatterns = [
    path('chat/',ChatApiView.as_view()),
    path('history/<str:session_key>/',ChatHistory.as_view()),
]
