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
from accounts.permissions import IsActiveUsers
from notification.services import create_notification

class CheckoutPreview(APIView):
    
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
            return Response({"error": "Invalid reservation"})

        data = calculate_booking_amount(reservations)

        return Response(data)



class CheckoutCartView(APIView):
    permission_classes =[IsActiveUsers]
    

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user,product__is_active=True,
                                         product__owner__is_live=True)\
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
                "min_days":item.product.min_rental_days, 
                "quantity": item.quantity,
                "image": first_image  
            })

        return Response(data)



def is_product_available(product, start, end, user=None):
    
    total_days = (end-start).days
    
    if total_days < product.min_rental_days:
        return {
            'available':False,
            'error':f"Minimum {product.min_rental_days} days required for this product"
        }

    booked = Booked_items.objects.filter(
        Q(product=product) &
        Q(start_date__lt=end) &
        Q(end_date__gt=start)&
        Q(status__in=['PENDING','DELIVERED','CONFIRMED'])
    )

    reserved = Reservation.objects.filter(
        Q(product=product) &
        Q(start_date__lt=end) &
        Q(end_date__gt=start) &
        Q(is_paid=False) &
        Q(expires_at__gt=timezone.now())
    )

    if user:
        reserved = reserved.exclude(user=user)

    return {
        'available': not (booked.exists() or reserved.exists())
    }



from .utils import calculate_amount_for_items,calculate_amount_from_reservations
class CheckAvailabilityView(APIView):
    permission_classes =[IsActiveUsers]
    

    def post(self, request):

        cart_id = request.data.get("cart_id")
        start = request.data.get("start_date")
        end = request.data.get("end_date")

        # if not cart_id or not start or not end:
        #     return Response({"error": "Missing fields"})
        
        if not cart_id:
            return Response({"error": "Missing cart"})
        if not start:
            return Response({"error": "Missing start-date"})
        if not end:
            
            return Response({"error": "Missing end-date"})
            

        try:
            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()
        except:
            return Response({"error": "Invalid date format"})
        now =timezone.now().date()
        
        if start < now:
            return Response({'error':'Starting date not be past . poda awdn'})
        
        if start >= end:
            return Response({"error": "End date must be after start date"})

        cart_item = Cart.objects.filter(
            id=cart_id,
            user=request.user
        ).select_related('product').first()

        if not cart_item:
            return Response({"error": "Cart not found"})
        
        if not cart_item.product.is_active:
            return Response({"error":f"{cart_item.product.title } is unavailable"})
        
        if not cart_item.product.owner.is_live:
            return Response({"error":f" owner unavailable for {cart_item.product.title }"})

        result = is_product_available(
            cart_item.product,
            start,
            end,
            request.user
        )
        
        if not result['available']:
            return Response(result,status=200)
        
        amount = calculate_amount_for_items(
            [{
                'product':cart_item.product,
                'quantity':cart_item.quantity,
                'start':start,
                'end':end
            }]
        )
        
        amount['delivery'] =0
        amount['grand_total'] =(
            amount['rent'] + amount['deposit'] + amount['tax'] + amount['convenience']
        )

        return Response({
            'available':True,
            'note':'Delivery calculated at checkout',
            **amount,
        })
        






def calculate_booking_amount(reservations):
    
        total_rent = sum(r.total_rent for r in reservations)
        total_deposit = sum(r.total_deposit for r in reservations)
        
        tax = total_rent * 0.18
        convenience = total_rent * 0.10
        
        if total_rent>35000:
            delivery = 0
        elif total_rent > 20000:
            delivery =200
        elif total_rent>10000:
            delivery = 100
        else:
            delivery =500
        
        grand_total = total_rent+total_deposit+tax+convenience+delivery 
        
        return {
            'rent':total_rent,
            'deposit':total_deposit,
            'tax':tax,
            'convenience':convenience,
            'delivery':delivery,
            'grand_total':grand_total
            
        }
    
     
       

from django.db import transaction
 
class CreateBookingReservationView(APIView):
    permission_classes =[IsActiveUsers]
    
    
    
    @transaction.atomic
    def post(self, request):

        user = request.user
        items = request.data.get("items", [])  #pass in  frontend 
        address_id = request.data.get('address_id')

        if not items:
            return Response({"error": "No items provided"})
        
        if  not Address.objects.filter(id=address_id,user=user).exists():
            return Response({'error':'invalid address'})

        reservations = set()
        # grand_rent = 0
        # grand_deposit = 0
        amount_items =[]
        validated_items =[]

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
                return Response({"error": f"Cart items not found"},status=400)
            
            if not cart_item.product.is_active:
                return Response({"error":f"{cart_item.product.title } is unavailable"},status=400)
        
            if not cart_item.product.owner.is_live:
                return Response({"error":f" owner unavailable for {cart_item.product.title }"},status=400)


            # 🔥 availability check (booking + reservation)
            avail = is_product_available(cart_item.product, start, end, user)
            if not avail['available']:
                return Response({
                    "error": f"{cart_item.product.title} not available"
                },status=400)
                
            validated_items.append({
                "cart_item":cart_item,
                "start":start,
                "end":end
            })
            
        for data in validated_items:
            
            cart_item = data['cart_item']
            start=data['start']
            end = data['end']

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
                # grand_rent += existing.total_rent
                # grand_deposit += existing.total_deposit
                # continue
                amount_items.append({
                    'product':cart_item.product,
                    'quantity':cart_item.quantity,
                    'start':start,
                    'end':end
                })
                
                continue
            else:

                total_days = (end - start).days

                rent = cart_item.product.price_per_day * total_days * cart_item.quantity
                deposit = cart_item.product.security_deposit * cart_item.quantity
                
                amount_items.append({
                    'product':cart_item.product,
                    'quantity':cart_item.quantity,
                    'start':start,
                    'end':end
                })

                reservation = Reservation.objects.create(
                    user=user,
                    product=cart_item.product,
                    address_id=address_id,
                    start_date=start,
                    end_date=end,
                    quantity=cart_item.quantity,
                    total_rent=rent,
                    total_deposit=deposit,

                    expires_at=timezone.now() + timedelta(minutes=10),
                    is_paid=False
                )

                reservations.add(reservation.id)
                # grand_rent += rent
                # grand_deposit += deposit
        
        amount = calculate_amount_for_items(amount_items)

        return Response({
            "reservation_ids": list(reservations),
            # "total_rent": grand_rent,
            # "total_deposit": grand_deposit,
            # "total_payable": grand_rent + grand_deposit
            **amount,
        })




    
    
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .pagination import CustomPagination



class UserBookingCancelView(APIView):
    

    def patch(self, request):

        item_id = request.data.get('item_id')

        if not item_id:

            return Response({
                'error': 'item_id required'
            }, status=400)

        booked_item = Booked_items.objects.filter(
            id=item_id,
            booking__user=request.user
        ).select_related(
            'booking',
            'product'
        ).first()

        if not booked_item:

            return Response({
                'error': 'Booked item not found'
            }, status=404)

        # only allow before shipped

        if booked_item.status not in [
            'PENDING',
            'CONFIRMED'
        ]:

            return Response({
                'error': (
                    'Cannot cancel after shipment. '
                    'Please contact customer care.'
                )
            }, status=400)

        # cancel item

        booked_item.status = 'CANCELLED'
        booked_item.save()

        # notify owner

        create_notification(
            sender=request.user,

            receiver=booked_item.product.owner,

            notification_type='ORDER',

            title=(
                f'{request.user.username} cancelled '
                f'{booked_item.product.title}'
            ),

            message=(
                f'Order item cancelled by '
                f'{request.user.username}'
            ),

            redirect_url='/bookings/'
        )

        return Response({
            'msg': 'Booked item cancelled successfully'
        }, status=200)       



class Bookinglistview(ListAPIView):

    serializer_class = BookingSerializer
    pagination_class = CustomPagination

    def get_queryset(self):

        return Booking.objects.filter(
            user=self.request.user,
            items__status__in=[
                'PENDING',
                'CONFIRMED',
                'SHIPPED',
                'DELIVERED'
            ]
        ).select_related(
            'user',
            'address'
        ).prefetch_related(
            'items',
            'items__product'
        ).distinct()  
     
     
     
     
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
    

    