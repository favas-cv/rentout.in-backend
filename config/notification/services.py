from .models import Notification,UserFCMToken
from .firebase_service import send_push_notification


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def create_notification(
    sender,
    receiver,
    notification_type,
    title,
    message,
    redirect_url=None
):
    
    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        notification_type=notification_type,
        title=title,
        message=message,
        redirect_url=redirect_url
    )
    
    
    tokens = UserFCMToken.objects.filter(
        user=receiver
        
    )
    
    for token_obj in tokens:
        send_push_notification(
            token_obj.token,
            title,
            message
        )
        
        
    # channel_layer = get_channel_layer()

    # async_to_sync(channel_layer.group_send)(
    #     f"notifications_{receiver.id}",
    #     {
    #         "type": "send_notification",

    #         "data": {
    #             "id": notification.id,
    #             "title": notification.title,
    #             "message": notification.message,
    #             "notification_type": notification.notification_type,
    #             "redirect_url": notification.redirect_url,
    #             "is_read": notification.is_read,
    #             "created_at": str(notification.created_at),
    #         }
    #     }
    # )
    return notification


