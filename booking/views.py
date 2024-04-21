from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Doctor, Appointment, Payment
from .serializers import DoctorSerializer, AppointmentSerializer, PaymentSerializer

"""
Doctor View
"""


@extend_schema(
    request=DoctorSerializer,
    methods=["POST"]
)
@api_view(['GET', 'POST'])
def doctors(request):
    """
    List all doctors or create a new doctor
    :param request:
    :return:
    """
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def doctor_detail(request, doctor_id):
    """
    Retrieve, update or delete a doctor
    :param request:
    :param doctor_id:
    :return:
    """
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Appointment View
"""


@extend_schema(
    request=AppointmentSerializer,
    methods=["POST"]
)
@api_view(['POST', 'GET'])
def appointments(request):
    """
    List all appointments
    :param request:
    :return:
    """
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=AppointmentSerializer,
    methods=["PUT"]
)
@api_view(['GET', 'PUT', 'DELETE'])
def appointment_detail(request, appointment_id):
    """
    Retrieve, update or delete an appointment
    :param request:
    :param appointment_id:
    :return:
    """
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Payment View
"""


@extend_schema(
    request=PaymentSerializer,
    methods=["POST"]
)
@api_view(['POST'])
def make_payment(request):
    """
    Make Payment
    :param request:
    :return:
    """
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def payment_detail(request, payment_id):
    """
    Get Payment Details
    :param request:
    :param payment_id:
    :return:
    """
    try:
        payment = get_object_or_404(Payment, id=payment_id)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
