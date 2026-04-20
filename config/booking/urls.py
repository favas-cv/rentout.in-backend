from django.urls import path
from .views import( PreviousBookeditemsview,Bookinglistview,
                   BookingDetailedView,CreateBookingReservationView,
                   CheckAvailabilityView,CheckoutCartView
                   
                   )


urlpatterns = [
    path('checkout/',CheckoutCartView.as_view()),
    path('check-availability/',CheckAvailabilityView.as_view()),
    
    path('create-reservation/',CreateBookingReservationView.as_view()),
    path('list/',Bookinglistview.as_view()),
    path('list/<int:pk>/',BookingDetailedView.as_view()),
    path('prev-items/',PreviousBookeditemsview.as_view()),
    
]
    