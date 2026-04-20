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

class CreateRazorPayOrder(APIView):

    def post(self, request):
        reservation_ids = request.data.get("reservation_ids")

        reservations = Reservation.objects.filter(
            id__in=reservation_ids,
            user=request.user,
            is_paid=False
        )

        if not reservations:
            return Response({'error': 'Invalid reservation'})

        total = sum(r.total_rent + r.total_deposit for r in reservations)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": int(total * 100),
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
        
        

class VerifyPaymentView(APIView):

    @transaction.atomic
    def post(self, request):

        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
        except:
            return Response({"error": "Payment verification failed"})

        reservations = Reservation.objects.filter(
            razorpay_order_id=razorpay_order_id,
            user=request.user,
            is_paid=False
        )

        if not reservations:
            return Response({"error": "Reservation not found"})

        # ✅ Create booking
        address = Address.objects.filter(
            id=request.data.get("address_id")
        ).first()

        booking = Booking.objects.create(
            user=request.user,
            address=address,
            payment_id=razorpay_payment_id
        )

        total_rent = 0
        total_deposit = 0

        for r in reservations:

            # 🔥 re-check availability (race condition safety)
            if Booked_items.objects.filter(
                product=r.product,
                start_date__lt=r.end_date,
                end_date__gt=r.start_date
          ).exists():
                raise Exception("Item became unavailable")

            Booked_items.objects.create(
                booking=booking,
                product=r.product,
                start_date=r.start_date,
                end_date=r.end_date,
                booked_time_price=r.product.price_per_day,
                booked_time_deposit=r.product.security_deposit,
                quantity=r.quantity
            )

            total_rent += r.total_rent
            total_deposit += r.total_deposit

            r.is_paid = True
            r.save()

        booking.total_rent_money = total_rent
        booking.total_deposit_money = total_deposit
        booking.total_paid = total_rent + total_deposit
        booking.save()

        # 🧹 clear cart + reservation
        Cart.objects.filter(user=request.user).delete()
        reservations.delete()

        return Response({
            "msg": "Payment success & booking confirmed",
            "booking_id": booking.id
        })