from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adminpanel.models import Booking
from .models import Order
from .serializers import *
from rest_framework import viewsets


@api_view(['POST'])
def CreateOrder(request):
        data = request.data

        try:
                booking = Booking.objects.get(id=data['booking_id'])
        except Booking.DoesNotExist:
                return Response({'error': 'Booking not found'}, status=404)

        order = Order.objects.create(
                booking=booking,
                name=data['name'],
                email=data['email'],
                contact_no=data['contact_no']
        )

        serializer = OrderSerializer(order, many=False)

        return Response(serializer.data, status=201)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
