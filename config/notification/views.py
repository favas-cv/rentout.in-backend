import config.firebase

from django.shortcuts import render

from .models import Notification,UserFCMToken
from .serializers import UserFCMTokenSerializer,NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class SaveFCMTokenView(APIView):


    def post(self, request):

        token = request.data.get('token')

        if not token:
            return Response(
                {'error': 'Token required'},
                status=400
            )

        # remove old token from other users
        UserFCMToken.objects.filter(
            token=token
        ).delete()

        # create/update token for current user
        UserFCMToken.objects.update_or_create(
            user=request.user,
            defaults={
                'token': token
            }
        )

        return Response({
            'message': 'FCM token saved'
        })
        
        
        
class NotificationListView(APIView):


    def get(self, request):

        notifications = Notification.objects.filter(
            receiver=request.user
        ).exclude(notification_type='MESSAGE')

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    
    def patch(self,request,pk):
        notification = Notification.objects.filter(id=pk,receiver=request.user).first()
        if not notification:
            return Response({'error':'not notfication found '})
        
        notification.is_read=True
        notification.save()
        
        return Response({
            'msg':'marked as read'
        })
        
class MarkNotificationFullReadView(APIView):
    
    def patch(self,request):
        
        Notification.objects.filter(receiver = request.user , is_read=False).update(is_read=True)
        
        return Response({
            'msg':'all mark as read'
        })