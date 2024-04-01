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
            room_id = booking_data.get('room_id')
            start_date = booking_data.get('start_date')
            end_date = booking_data.get('end_date')

            # Check if the room is available
            room = get_object_or_404(Room, id=room_id)
            overlapping_bookings = room.bookings.filter(start_date__lt=end_date, end_date__gt=start_date)

            if not overlapping_bookings.exists():
                Booking.objects.create(
                    room=room,
                    order=order,
                    start_date=start_date,
                    end_date=end_date
                )
            else:
                transaction.set_rollback(True)
                return Response({'error': f"Room {room.id} not available for the given dates"}, status=400)

        return Response(OrderSerializer(order).data, status=201)
    else:
        return Response(order_serializer.errors, status=400)
