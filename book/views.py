from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adminpanel.models import Booking, Room
from filters.serializers import BookingSerializer
from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets
import logging


# @api_view(['POST'])
# def CreateOrder(request):
#         data = request.data
#
#         try:
#                 booking = Booking.objects.get(id=data['booking_id'])
#         except Booking.DoesNotExist:
#                 return Response({'error': 'Booking not found'}, status=404)
#
#         order = Order.objects.create(
#                 booking=booking,
#                 name=data['name'],
#                 email=data['email'],
#                 contact_no=data['contact_no']
#         )
#
#         serializer = OrderSerializer(order, many=False)
#
#         return Response(serializer.data, status=201)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.atomic
def create_order(request):
    data = request.data
    order_serializer = OrderSerializer(data=data.get('order'))
    if order_serializer.is_valid():
        order = order_serializer.save()
        booking_data_list = data.get('bookings')

        for booking_data in booking_data_list:
            # You should check here if the room_id in booking_data actually exists
            # and is available for the given dates.
            room = get_object_or_404(Room, id=booking_data.get('room_id'), is_available=True)

            # Check if the room is actually available for the dates requested
            if room.bookings.filter(start_date__lt=booking_data.get('end_date'),
                                    end_date__gt=booking_data.get('start_date')).exists():
                transaction.set_rollback(True)
                return Response({'error': f"Room {room.id} not available for the given dates"}, status=400)

            # Create a booking for the room and order
            Booking.objects.create(
                room=room,
                order=order,
                start_date=booking_data['start_date'],
                end_date=booking_data['end_date']
            )
            # Mark the room as unavailable if necessary
            room.is_available = False
            room.save()

        return Response(OrderSerializer(order).data, status=201)
    else:
        return Response(order_serializer.errors, status=400)
