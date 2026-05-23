from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def test_task():
    print("🔥 Celery is working!")
    
    
    
@shared_task
def send_welcome_mail(email):
    
    sub='Furnish your space without the commitment'
    
    msg = """
    Thank you for registering can now start browsing listings or list your own items for rent.


    Regards,


    The RentOut Team
    
    
    """
    
    send_mail(
        sub,msg,
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
    