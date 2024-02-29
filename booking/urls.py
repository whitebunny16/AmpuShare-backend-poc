from django.urls import path

from .views import *

urlpatterns = [
    path('booking-detail', get_booking_detail),
    path('create-booking', create_booking),
]
