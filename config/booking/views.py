from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .serializers import BookingSerializer,BookedItemsSerializer

from django.db import transaction
from .models import Booking, Booked_items,Reservation
from cart.models import Cart
from django.utils import  timezone

from .tasks import booking_successfull
from address.models import Address
from datetime import datetime,timedelta



class CheckoutCartView(APIView):

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)\
            .select_related('product')\
            .prefetch_related('product__images')  # 🔥 important

        data = []

        for item in cart_items:
            images = item.product.images.all()

            first_image = images[0].image_url if images else None

            data.append({
                "cart_id": item.id,
                "product_name": item.product.title,
                "price_per_day": item.product.price_per_day,
                "deposit": item.product.security_deposit,
                "quantity": item.quantity,
                "image": first_image  
            })

        return Response(data)



def is_product_available(product, start, end, user=None):

    booked = Booked_items.objects.filter(
        Q(product=product) &
        Q(start_date__lt=end) &
        Q(end_date__gt=start)
    )

    reserved = Reservation.objects.filter(
        Q(product=product) &
        Q(start_date__lt=end) &
        Q(end_date__gt=start) &
        Q(is_paid=False) &
        Q(expires_at__gt=timezone.now())
    )

    # if user:
    #     reserved = reserved.exclude(user=user)

    return not (booked.exists() or reserved.exists())




class CheckAvailabilityView(APIView):

    def post(self, request):

        cart_id = request.data.get("cart_id")
        start = request.data.get("start_date")
        end = request.data.get("end_date")

        if not cart_id or not start or not end:
            return Response({"error": "Missing fields"})

        try:
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
        except:
            return Response({"error": "Invalid date format"})

        if start >= end:
            return Response({"error": "End date must be after start date"})

        cart_item = Cart.objects.filter(
            id=cart_id,
            user=request.user
        ).select_related('product').first()

        if not cart_item:
            return Response({"error": "Cart not found"})

        available = is_product_available(
            cart_item.product,
            start,
            end,
            request.user
        )

        return Response({
            "available": available
        })
        
        

class CreateBookingReservationView(APIView):

    def post(self, request):

        user = request.user
        items = request.data.get("items", [])  #pass in  frontend 

        if not items:
            return Response({"error": "No items provided"})

        reservations = set()
        grand_rent = 0
        grand_deposit = 0

        for item in items:

            cart_id = item.get("cart_id")
            start = item.get("start_date")
            end = item.get("end_date")

            if not cart_id or not start or not end:
                return Response({"error": "Missing fields"})

            try:
                start = datetime.strptime(start, "%Y-%m-%d").date()
                end = datetime.strptime(end, "%Y-%m-%d").date()
            except:
                return Response({"error": "Invalid date format"})

            if start >= end:
                return Response({"error": "Invalid date range"})

            cart_item = Cart.objects.filter(
                id=cart_id,
                user=user
            ).select_related('product').first()

            if not cart_item:
                return Response({"error": f"Cart item {cart_id} not found"})

            # 🔥 availability check (booking + reservation)
            if not is_product_available(cart_item.product, start, end, user):
                return Response({
                    "error": f"{cart_item.product.title} not available"
                })

            # 🔥 prevent duplicate reservation (same user + product + date)
            existing = Reservation.objects.filter(
                user=user,
                product=cart_item.product,
                start_date=start,
                end_date=end,
                is_paid=False,
                expires_at__gt=timezone.now()
            ).first()

            if existing:
                reservations.add(existing.id)
                grand_rent += existing.total_rent
                grand_deposit += existing.total_deposit
                continue

            total_days = (end - start).days

            rent = cart_item.product.price_per_day * total_days * cart_item.quantity
            deposit = cart_item.product.security_deposit * cart_item.quantity

            reservation = Reservation.objects.create(
                user=user,
                product=cart_item.product,
                start_date=start,
                end_date=end,
                quantity=cart_item.quantity,
                total_rent=rent,
                total_deposit=deposit,
                expires_at=timezone.now() + timedelta(minutes=10),
                is_paid=False
            )

            reservations.add(reservation.id)
            grand_rent += rent
            grand_deposit += deposit

        return Response({
            "reservation_ids": list(reservations),
            "total_rent": grand_rent,
            "total_deposit": grand_deposit,
            "total_payable": grand_rent + grand_deposit
        })




    
    
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .pagination import CustomPagination

class Bookinglistview(ListAPIView):
     
    
    serializer_class=BookingSerializer
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('user','address')
    
    pagination_class = CustomPagination
     
class BookingDetailedView(RetrieveAPIView):
    serializer_class =BookingSerializer
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related('items')


class PreviousBookeditemsview(ListAPIView):
    serializer_class = BookedItemsSerializer
    def get_queryset(self):
        # booking_id = self.kwargs.get('pk') 
        return Booked_items.objects.filter(booking__user=self.request.user).select_related('booking','product')
    pagination_class = CustomPagination
    

    