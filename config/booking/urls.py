from django.urls import path
from .views import( PreviousBookeditemsview,Bookinglistview,
                   BookingDetailedView,CreateBookingReservationView,
                   CheckAvailabilityView,CheckoutCartView,
                   CheckoutPreview,UserBookingCancelView
                   
                   )
from paymentsetup.views import CreateRazorPayOrder,VerifyPaymentView


urlpatterns = [
    path('checkout/',CheckoutCartView.as_view()),
    path('checkout-preview/',CheckoutPreview.as_view()), #dont need delete ater all set 
    path('check-availability/',CheckAvailabilityView.as_view()),
    
    path('create-reservation/',CreateBookingReservationView.as_view()),
    path('create-razorpay-order/',CreateRazorPayOrder.as_view()),
    path('verify-payment/',VerifyPaymentView.as_view()),
    path('list/',Bookinglistview.as_view()),
    path('list/<int:pk>/',BookingDetailedView.as_view()),
    path('prev-items/',PreviousBookeditemsview.as_view()),
    path('cancel/',UserBookingCancelView.as_view()),
     
]
      