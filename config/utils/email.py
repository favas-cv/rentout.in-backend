from django.core.mail import send_mail
from django.conf import settings
import random
from celery import shared_task


@shared_task
def send_otp_email(email,otp):
    
    subject ='Your OTP Verification code'
    
    message =f""" 
    Hello,
    Your otp is : {otp}
    
    this code is expire in 5 mminutes , do not share this code 
    
    regards,
    RentOut.in
    
    
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    
    print(otp)





def send_admin_kyc_email(result,user_id):
    
    subject = f"KYC Result of User {user_id}"
    message=f"""
    KYC STATUS : {result.get('status')}
    CONFIDENCE : {result.get('confidence')}
    
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_ADMIN_USER],
        fail_silently=False
    )
    
def send_user_rejection_kyc_mail(user):
    subject = f"KYV VERIFICATION IS FAILED"
    message="""
    Dear Customer,
    Sorry
    Your KYC Verification was rejected.
    Please upload clear and valid document and try again.
    If anything trouble please contact our customer care.
    thankyou
    
    
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )