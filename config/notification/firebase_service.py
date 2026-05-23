from firebase_admin import messaging
from .models import UserFCMToken

def send_push_notification(token, title, body):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token
    )

    try:
        messaging.send(message)

    except Exception as e:

        print(f"Error sending FCM notification: {e}")

        # remove invalid token
        UserFCMToken.objects.filter(
            token=token
        ).delete()