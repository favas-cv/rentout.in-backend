from django.shortcuts import render

import razorpay

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import Cart
from booking.models import Reservation
from django.db import transaction
from address.models import Address
from booking.models import Booked_items,Booking        
from booking.views import calculate_booking_amount
from notification.services import create_notification
from accounts.permissions import IsActiveUsers

class CreateRazorPayOrder(APIView):
    
    permission_classes =[IsActiveUsers]

    def post(self, request):
        reservation_ids = request.data.get("reservation_ids")
        if not reservation_ids or not isinstance(reservation_ids, list):
            return Response({"error": "reservation_ids must be a list"}, status=400)


        reservations = Reservation.objects.filter(
            id__in=reservation_ids,
            user=request.user, 
            is_paid=False
        )

        if not reservations:
            return Response({'error': 'Invalid reservation'})
        
        data = calculate_booking_amount(reservations)


        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": int(data['grand_total']*100),
            "currency": "INR",
            "payment_capture": 1
        })

        # store order id
        reservations.update(razorpay_order_id=order['id'])

        return Response({
            "order_id": order['id'],
            "amount": order['amount'],
            "key": settings.RAZORPAY_KEY_ID
        })
    
    
    
    
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import razorpay

from cart.models import Cart
from booking.models import Reservation, Booked_items, Booking
from booking.views import calculate_booking_amount
from notification.services import create_notification


class VerifyPaymentView(APIView):
    
    permission_classes =[IsActiveUsers]

    @transaction.atomic
    def post(self, request):

        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not all([
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        ]):
            return Response({
                "error": "Missing payment details"
            }, status=400)

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        # ---------------------------------------------------
        # DUPLICATE PAYMENT PROTECTION
        # ---------------------------------------------------

        existing_booking = Booking.objects.filter(
            payment_id=razorpay_payment_id
        ).first()

        if existing_booking:
            return Response({
                "msg": "Booking already verified",
                "booking_id": existing_booking.id
            })

        # ---------------------------------------------------
        # VERIFY PAYMENT SIGNATURE
        # ---------------------------------------------------

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

        except Exception:
            return Response({
                "error": "Payment verification failed"
            }, status=400)

        # ---------------------------------------------------
        # LOCK RESERVATIONS
        # ---------------------------------------------------

        reservations = Reservation.objects.select_for_update().filter(
            razorpay_order_id=razorpay_order_id,
            user=request.user,
            is_paid=False
        ).select_related(
            'product',
            'address'
        )

        if not reservations.exists():
            return Response({
                "error": "Reservation not found or expired"
            }, status=404)

        first_reservation = reservations.first()
        address = first_reservation.address

        if not address:
            return Response({
                "error": "Address missing"
            }, status=400)

        reservation_ids = list(
            reservations.values_list('id', flat=True)
        )

        # ---------------------------------------------------
        # FINAL AVAILABILITY CHECK
        # ---------------------------------------------------

        for r in reservations:
            
            if not r.product.is_active:

                try:
                    client.payment.refund(
                        razorpay_payment_id
                    )
                except:
                    pass

                reservations.delete()

                return Response({
                    "error": (
                        f"{r.product.title} is unavailable now. "
                        f"Amount refunded."
                    )
                }, status=400)


            if not r.product.owner.is_live:

                try:
                    client.payment.refund(
                        razorpay_payment_id
                    )
                except:
                    pass

                reservations.delete()

                return Response({
                    "error": (
                        f"Owner unavailable for "
                        f"{r.product.title}. "
                        f"Amount refunded."
                    )
                }, status=400)

            overlap = Booked_items.objects.filter(
                product=r.product,
                start_date__lt=r.end_date,
                end_date__gt=r.start_date,
                status__in=[
                    'PENDING',
                    'CONFIRMED',
                    'DELIVERED'
                ]
            ).exists()

            if overlap:

                # REFUND PAYMENT
                try:
                    client.payment.refund(
                        razorpay_payment_id
                    )
                except:
                    pass

                # DELETE RESERVATIONS
                reservations.delete()

                return Response({
                    "error": f"{r.product.title} became unavailable. Amount refunded."
                }, status=400)

        # ---------------------------------------------------
        # CREATE BOOKING
        # ---------------------------------------------------

        booking = Booking.objects.create(
            user=request.user,
            address=address,

            address_snapshot={
                'house_name': address.house_name,
                'street': address.street,
                'state': address.state,
                'phone': address.phone,
                'zipcode': address.zipcode
            },

            payment_id=razorpay_payment_id
            # status='PENDING'
        )

        # ---------------------------------------------------
        # CREATE BOOKED ITEMS
        # ---------------------------------------------------

        for r in reservations:

            first_image_obj = r.product.images.first()

            image = (
                first_image_obj.image_url
                if first_image_obj else None
            )

            Booked_items.objects.create(
                booking=booking,
                product=r.product,

                product_snapshot={
                    'title': r.product.title,
                    'locality': r.product.locality,
                    'price_per_day': r.product.price_per_day,
                    'deposit': r.product.security_deposit,
                    'image': image
                },

                start_date=r.start_date,
                end_date=r.end_date,
                quantity=r.quantity,
                status='PENDING',
                deposit_status='PENDING'
            )

        # ---------------------------------------------------
        # CALCULATE TOTALS
        # ---------------------------------------------------

        data = calculate_booking_amount(reservations)

        booking.total_rent_money = data['rent']
        booking.total_deposit_money = data['deposit']
        booking.tax_amount = data['tax']
        booking.convenience_charge = data['convenience']
        booking.delivery_package_charge = data['delivery']
        booking.total_paid = data['grand_total']

        booking.save()

        # ---------------------------------------------------
        # MARK RESERVATION PAID
        # ---------------------------------------------------

        reservations.update(is_paid=True)

        # ---------------------------------------------------
        # SEND OWNER NOTIFICATIONS
        # ---------------------------------------------------

        owners = set()

        for r in reservations:
            owners.add(r.product.owner)

        for owner in owners:

            create_notification(
                sender=request.user,
                receiver=owner,

                notification_type='NEW_BOOKING',

                title='New Booking Received',

                message=(
                    f'{request.user.username} '
                    f'booked your product'
                ),

                redirect_url='/owner/bookings/'
            )

        # ---------------------------------------------------
        # CLEAR CART & RESERVATIONS
        # ---------------------------------------------------

        Cart.objects.filter(
            user=request.user
        ).delete()

        Reservation.objects.filter(
            id__in=reservation_ids
        ).delete()

        # ---------------------------------------------------
        # SUCCESS RESPONSE
        # ---------------------------------------------------

        return Response({
            "msg": "Payment success & booking confirmed",
            "booking_id": booking.id
        })    

# class VerifyPaymentView(APIView):

#     @transaction.atomic
#     def post(self, request):

#         razorpay_order_id = request.data.get("razorpay_order_id")
#         razorpay_payment_id = request.data.get("razorpay_payment_id")
#         razorpay_signature = request.data.get("razorpay_signature")
        
#         if not all([
#             razorpay_order_id,
#             razorpay_payment_id,
#             razorpay_signature
#         ]):
#             return Response({"error":"missing payment details"},status=400)
        
        

#         client = razorpay.Client(
#             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#         )
        
        
        
#         existing_booking = Booking.objects.filter(
#             payment_id=razorpay_payment_id
#         ).first()

#         if existing_booking:
#             return Response({
#                 "msg": "Booking already verified",
#                 "booking_id": existing_booking.id
#             })
        
        

#         try:
#             client.utility.verify_payment_signature({
#                 "razorpay_order_id": razorpay_order_id,
#                 "razorpay_payment_id": razorpay_payment_id,
#                 "razorpay_signature": razorpay_signature
#             })
#         except:
#             return Response({"error": "Payment verification failed"})




#         reservations = Reservation.objects.filter(
#             razorpay_order_id=razorpay_order_id,
#             user=request.user,
#             is_paid=False
#         ).select_related(
#             'product',
#             'address'
#         )

#         if not reservations:
#             return Response({"error": "Reservation not found or expired"},status=404)
        
#         first_reservation = reservations.first()
#         address = first_reservation.address
        
#         if not address:
#             return Response({'error':'Address is missing in reservation'})
        

       

#         booking = Booking.objects.create(
#             user=request.user,
#             address=address,
#             address_snapshot={
#                 'house_name':address.house_name,
#                 'street':address.street,
#                 'state':address.state,
#                 'phone':address.phone,
#                 'zipcode':address.zipcode
 
#             },
#             payment_id=razorpay_payment_id
#         )

#         reservation_ids = list(reservations.values_list('id', flat=True))
        
#         for r in reservations:

#             # 🔥 re-check availability (race condition safety)
#             if Booked_items.objects.filter(
#             product=r.product,
#             start_date__lt=r.end_date,
#             end_date__gt=r.start_date,
#             booking__status__in=['PENDING','CONFIRMED','DELIVERED']
#         ).exists():
#                 return Response({"error":"Item became unavailable sry "})
            
#             first_image_obj = r.product.images.first()
#             image = first_image_obj.image_url if first_image_obj else None

#             Booked_items.objects.create( 
#                 booking=booking,
#                 product=r.product,
#                 product_snapshot={
#                     'title':r.product.title,
#                     'locality':r.product.locality,
#                     'price_per_day':r.product.price_per_day,
#                     'deposit':r.product.security_deposit,
#                     'image':image
#                     },
#                 start_date=r.start_date,
#                 end_date=r.end_date,

#                 quantity=r.quantity
#             )

#             # r.is_paid = True
#             # r.save()

#         data = calculate_booking_amount(reservations)
        
#         booking.total_rent_money = data['rent']
#         booking.total_deposit_money = data['deposit']
#         booking.tax_amount = data['tax']
#         booking.convenience_charge = data['convenience']
#         booking.delivery_package_charge = data['delivery']
#         booking.total_paid = data['grand_total']
        
#         booking.save()
        
#         owners = set()
#         for r in reservations:
#             owners.add(r.product.owner)
        
#         for owner in owners:
#             create_notification(
#             sender=request.user,
#             receiver=owner,
#             notification_type='NEW_BOOKING',
#             title='New Booking Received',
#             message=f'{request.user.username} booked your product',
#             redirect_url='/owner/bookings/'
#         )
            
        
        

#         # 🧹 clear cart + reservation
#         Cart.objects.filter(user=request.user).delete()
#         Reservation.objects.filter(id__in=reservation_ids).delete()

#         return Response({
#             "msg": "Payment success & booking confirmed",
#             "booking_id": booking.id
#         })