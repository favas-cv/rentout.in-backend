from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Reservation
from django.utils import timezone

@shared_task
def booking_successfull(email,username):
    
    send_mail(
        f"kollam kollaam mr {username}",
        'you booked an item fromus thanku=you for ur booking and dashh..',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
        
    
    )
    
    

@shared_task
def delete_expired_reservations():
    print("🔥 TASK EXECUTED 🔥")
    deleted_count, _ = Reservation.objects.filter(
        expires_at__lt=timezone.now(),
        is_paid=False
    ).delete()

    return f"Deleted {deleted_count} expired reservations"
     
    