
from rest_framework import serializers
from kyc.models  import KycDocs

from products.models import Product
from utils.email import send_product_blocked_mail,send_user_blocked_mail
from accounts.models import User


# KYC SERIALIZERS


from notification.services import create_notification

class KYCStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = KycDocs 
        fields = ['id', 'status']

    def update(self, instance, validated_data):

        old_status = instance.status

        new_status = validated_data.get(
            'status',
            instance.status
        )

        allowed_transitions = {
            'PENDING': ['VERIFIED', 'REJECTED', 'REVIEW'],
            'REVIEW': ['VERIFIED', 'REJECTED'],
            'VERIFIED': ['REJECTED'],
            'REJECTED': ['VERIFIED']
        }

        if new_status != old_status:

            if new_status not in allowed_transitions.get(old_status, []):

                raise serializers.ValidationError(
                    f"Cannot change status from {old_status} to {new_status}"
                )

        instance.status = new_status

        instance.save()
        
        
        if new_status == 'VERIFIED':
            
            instance.approve()
            
        elif new_status =='REJECTED':
            
            instance.reject()
        
        elif new_status =='REVIEW':
            
            instance.review()

 
        if old_status != new_status:

            create_notification(
                sender=self.context['request'].user,
                receiver=instance.user,
                notification_type='KYC_STATUS_UPDATE',
                title=f"KYC status updated to {new_status}",
                message=f"Your KYC verification is now {new_status}",
                redirect_url='/my-kyc/'
            )

        return instance

        







# PRODUCT SERIALIZERS



class AdminProductSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Product
        fields = '__all__'
        
    
    def update(self,instance,validated_data):
        
        old_active_status = instance.is_active
        
        new_active_status = validated_data.get('is_active',instance.is_active)
        
        
        instance.is_active = new_active_status
        
        instance.is_featured = validated_data.get(
            'is_featured',
            instance.is_featured
        )

        instance.is_trending = validated_data.get(
            'is_trending',
            instance.is_trending
        )

        instance.is_seasonal = validated_data.get(
            'is_seasonal',
            instance.is_seasonal
        )
        
        instance.save()
        
        if old_active_status and not new_active_status:
            send_product_blocked_mail.delay(instance.id)
        
        return instance



# USERS serializers




class AdminUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','email','is_owner','is_live','profile_pic']
        
        
    def update(self,instance,validated_data):
        
        old_active_status = instance.is_live
        
        new_active_status = validated_data.get('is_live',instance.is_live)
        
        instance.is_live = new_active_status
        
        instance.save()
        
        if old_active_status and not new_active_status:
            send_user_blocked_mail.delay(instance.id)
        
        return instance
            
        
    


        
        
        
        







