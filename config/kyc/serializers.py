from rest_framework import serializers
from .models import KycDocs
import cloudinary.uploader
# from .tasks import call_kyc_verification

class KycSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(source ='user.username',read_only =True)
    email=serializers.CharField(source ='user.email',read_only =True)
    
    class Meta:
        model =KycDocs
        fields='__all__'


class KycDocsSerializer(serializers.ModelSerializer):

    document1 = serializers.ImageField(write_only=True)
    document2 = serializers.ImageField(write_only=True)
    selfie = serializers.ImageField(write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = KycDocs  
        fields = '__all__'

    def create(self, validated_data):

        user = validated_data.get('user')

        doc1 = validated_data.pop('document1')
        doc2 = validated_data.pop('document2')
        selfie = validated_data.pop('selfie')

        upload1 = cloudinary.uploader.upload(doc1, folder='verification_docs').get('secure_url')
        upload2 = cloudinary.uploader.upload(doc2, folder='verification_docs').get('secure_url')
        upload3 = cloudinary.uploader.upload(selfie, folder='verification_selfie').get('secure_url')

        docs, created = KycDocs.objects.update_or_create(
            user=user,  # ✅ lookup field
            defaults={
                "document1": upload1,
                "document2": upload2,
                "selfie": upload3,
                # "status": "pending"
            }
        )
        # call_kyc_verification.delay(user.id)
        
        

        return docs
    