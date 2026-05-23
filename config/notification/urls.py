from .views import NotificationListView,SaveFCMTokenView,MarkNotificationFullReadView,MarkNotificationReadView
from django.urls import path

urlpatterns = [
    path('',NotificationListView.as_view()),
    path('read-all/',MarkNotificationFullReadView.as_view()),
    path('<int:pk>/read/',MarkNotificationReadView.as_view()),
    path('save-token/',SaveFCMTokenView.as_view()),
    
]


