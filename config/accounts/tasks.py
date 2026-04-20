from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def test_task():
    print("🔥 Celery is working!")
    
    
    
@shared_task
def send_welcome_mail(email):
    send_mail(
        'welcome to renout.in',
        'thankyou for registeiring',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
        
    )
    
@shared_task 
def logoutmail(email):
    send_mail(
        'bye bye from renout.in',
        'thankyou for logouting',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
        
    )
    