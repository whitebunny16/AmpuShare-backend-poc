from django.urls import path

from .views import *

urlpatterns = [
    # Doctor
    path('doctors/', doctors),
    path('doctors/<str:doctor_id>', doctor_detail),

    # Appointment
    path('appointments/', appointments),
    path('appointments/<str:appointment_id>', appointment_detail),

    # Payment
    path('payments/', make_payment),
    path('payments/<str:payment_id>', payment_detail),
]
