# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from kyc.models import KycDocs
# from kyc.ai.pipeline import run_kyc_pipeline
# from utils.email import send_admin_kyc_email,send_user_rejection_kyc_mail

# @shared_task
# def call_kyc_verification(user_id):
#     try:
#         kyc = KycDocs.objects.filter(user=user_id).first()
#         if not kyc:
#             return {'error':'KYC not found'}
        
#         result = run_kyc_pipeline(kyc)
#         kyc.status=result.get('status')
#         kyc.save()
        
#         send_admin_kyc_email(result,kyc.user)
        
#         if result.get('status') == 'rejected':
#             send_user_rejection_kyc_mail(kyc.user)
        
#         return result
        
        
        
#     except KycDocs.DoesNotExist:
#         return {'error':'kyc not found'}
    
#     except Exception as e:
#         return {'error':str(e)}