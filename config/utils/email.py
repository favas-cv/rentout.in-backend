from django.core.mail import send_mail
from django.conf import settings
import random
from celery import shared_task
from products.models import Product
from accounts.models import User

@shared_task
def send_otp_email(email,otp):
    
    subject = "🔑 Your RentOut.in Verification Code"

    message = f"""Dear User,

    To complete your verification, please use the following One-Time Password (OTP):

    👉 {otp}

    This code is valid for the next 5 minutes. 

    ⚠️ SECURITY WARNING: 
    For your security, never share this code with anyone, including RentOut.in support agents. If you did not request this verification, please secure your account or disregard this email.

    Best regards,
    The RentOut.in Security Team
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
    

@shared_task
def send_product_blocked_mail(product_id):
    
    try:
        product=Product.objects.get(id=product_id)
    
    except Product.DoesNotExist:
        return 

    subject = "Your Product Has Been Temporarily Disabled"

    message = f"""
Dear {product.owner.username},

Your product "{product.title}" has been temporarily disabled by our admin team.

If you believe this was a mistake or need more information,
please contact our support team.

Thank you,
Support Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [product.owner.email],
        fail_silently=True
    )
    

@shared_task
def send_user_blocked_mail(user_id):
    
    try:
        user = User.objects.get(id=user_id)
    
    except User.DoesNotExist:
        return 
    

    subject = "Your Has Been Temporarily Disabled"

    message = f"""
Dear {user.username},

Your has been temporarily disabled by our admin team.

If you believe this was a mistake or need more information,
please contact our support team.

Thank you,
Support Team
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True
    )
    