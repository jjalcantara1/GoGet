from decimal import Decimal

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
from datetime import datetime


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
        total_cost = Decimal("0.00")  # Initialize total cost as Decimal

        for booking_data in booking_data_list:
            room_id = booking_data.get('room_id')
            start_date = booking_data.get('start_date')
            end_date = booking_data.get('end_date')

            # Calculate the number of nights
            num_nights = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days - 1
            num_nights = Decimal(num_nights)  # Ensure num_nights is a Decimal

            room = get_object_or_404(Room, id=room_id)
            overlapping_bookings = room.bookings.filter(start_date__lt=end_date, end_date__gt=start_date)

            if not overlapping_bookings.exists():
                Booking.objects.create(
                    room=room,
                    order=order,
                    start_date=start_date,
                    end_date=end_date
                )
                # Calculate the total cost for this booking and add to the total_cost
                total_cost += room.room_type.price * num_nights
            else:
                transaction.set_rollback(True)
                return Response({'error': f"Room {room.id} not available for the given dates"}, status=400)

        # Update the order with the calculated total cost
        order.total_cost = total_cost
        order.save()

        return Response(OrderSerializer(order).data, status=201)
    else:
        return Response(order_serializer.errors, status=400)
