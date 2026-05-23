from booking.models import Booking,Booked_items
from accounts.models import User

from rest_framework import serializers
from notification.services  import create_notification


class OwnerBookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booked_items
        fields = ['id','status', 'deposit_status']

    def update(self, instance, validated_data):
        old_status = instance.status
        old_deposit_status = instance.deposit_status
        order_id = instance.booking.id
        new_status = validated_data.get('status', instance.status)
        new_deposit_status = validated_data.get('deposit_status', instance.deposit_status)

        # -------- ORDER STATUS VALIDATION --------
        allowed_transitions = {
            'PENDING': ['CONFIRMED', 'CANCELLED'],
            'CONFIRMED': ['SHIPPED', 'CANCELLED'],
            'SHIPPED':['DELIVERED','CANCELLED'],
            'DELIVERED': ['RETURNED'],
            'RETURNED': [],
            'CANCELLED': [] 
        }

        current_status = instance.status

        if new_status != current_status:
            if new_status not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from {current_status} to {new_status}"
                ) 

        # -------- DEPOSIT STATUS VALIDATION --------
        deposit_transitions = {
            'PENDING': ['HOLD'],
            'HOLD': ['REFUND_INITIATED'],
            'REFUND_INITIATED': ['REFUNDED'],
            'REFUNDED': []
        }

        current_deposit = instance.deposit_status

        # ❗ Rule 1: Refund only after RETURNED
        if new_deposit_status in ['REFUND_INITIATED', 'REFUNDED']:
            if instance.status not in [ 'RETURNED','CANCELLED']:
                raise serializers.ValidationError(
                    "Deposit refund allowed only after product is returned or cancelled"
                )

        # ❗ Rule 2: Prevent changes after REFUNDED
        if current_deposit == 'REFUNDED':
            raise serializers.ValidationError(
                "Deposit already refunded. No further updates allowed"
            )

        # ❗ Rule 3: Transition validation
        if new_deposit_status != current_deposit:
            if new_deposit_status not in deposit_transitions.get(current_deposit, []):
                raise serializers.ValidationError(
                    f"Cannot change deposit status from {current_deposit} to {new_deposit_status}"
                )

        # -------- SAVE --------
        instance.status = new_status
        instance.deposit_status = new_deposit_status

        instance.save()
        
        if old_status != new_status:
            create_notification(
                sender=self.context['request'].user,
                receiver=instance.booking.user,
                notification_type='BOOKING_STATUS_UPDATE',
                title=f"Your Order ID({order_id} is {new_status})",
                message=f"Your product {instance.product.title} is now in {new_status}",
                redirect_url='/my-orders/'
            )
        
        if old_deposit_status !=new_deposit_status:
            create_notification(
                sender=self.context['request'].user,
                receiver=instance.booking.user,
                notification_type='DEPOSIT_STATUS_UPDATE',
                title=f"Your Order ID({order_id} deposit amount is {new_deposit_status})",
                message=f"Your security deposit for product {instance.product.title}  is now {new_deposit_status}, thankyou",
                redirect_url='/my-orders/'
            )
        return instance


class OwnerBookedItemsSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='booking.user.username',
        read_only=True
    )

    customer_email = serializers.CharField(
        source='booking.user.email',
        read_only=True
    )

    product_name = serializers.CharField(
        source='product.title',
        read_only=True
    )

    rate = serializers.IntegerField(
        source='product.price_per_day',
        read_only=True
    )

    image = serializers.SerializerMethodField()

    rented_days = serializers.SerializerMethodField()
    
    address_snapshot = serializers.SerializerMethodField()

    class Meta:

        model = Booked_items

        fields = [
            'id',

            'customer_name',
            'customer_email',

            'product_name',

            'rate',
            'image',

            'quantity',

            'start_date',
            'end_date',

            'rented_days',

            'status',
            'deposit_status',
            'address_snapshot',

            'created_at'
        ]

    def get_image(self, obj):

        first_image = obj.product.images.first()

        if first_image:
            return first_image.image_url

        return None

    def get_rented_days(self, obj):

        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days

        return 0
    
    def get_address_snapshot(self,obj):
        return obj.booking.address_snapshot