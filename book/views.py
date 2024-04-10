from decimal import Decimal

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from adminpanel.models import Booking, Room, SurchargeRates
from filters.serializers import BookingSerializer
from .models import Order
from .serializers import OrderSerializer
from rest_framework import viewsets
import logging
from datetime import datetime
from django.db.models import Sum, F


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
        today = datetime.today().date()  # Get today's date

        # Fetch surcharge rates
        surcharge_rates = SurchargeRates.objects.first()  # Assuming there's only one entry
        pet_friendly_surcharge = surcharge_rates.pet_friendly_surcharge if surcharge_rates else Decimal("100.00")
        smoking_surcharge = surcharge_rates.smoking_surcharge if surcharge_rates else Decimal("200.00")

        for booking_data in booking_data_list:
            room_id = booking_data.get('room_id')
            start_date_str = booking_data.get('start_date')
            end_date_str = booking_data.get('end_date')

            # Parse the dates from strings to date objects
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Check if the dates are in the past
            if start_date < today or end_date <= today:
                return Response({
                    'error': 'Cannot book dates in the past.'
                }, status=400)

            room = get_object_or_404(Room, id=room_id)
            overlapping_bookings = room.bookings.filter(start_date__lt=end_date, end_date__gt=start_date)

            if not overlapping_bookings.exists():
                # Calculate the number of nights
                num_nights = (end_date - start_date).days
                booking_cost = room.room_type.price * Decimal(num_nights)

                # Apply surcharges based on room attributes
                if room.is_pet_friendly:
                    booking_cost += pet_friendly_surcharge
                if room.is_smoking:
                    booking_cost += smoking_surcharge

                # Create the booking instance
                Booking.objects.create(
                    room=room,
                    order=order,
                    start_date=start_date,
                    end_date=end_date
                )

                total_cost += booking_cost
            else:
                transaction.set_rollback(True)
                return Response({'error': f"Room {room.id} not available for the given dates"}, status=400)

        # Update the order with the calculated total cost
        order.total_cost = total_cost
        order.save()

        return Response(OrderSerializer(order).data, status=201)
    else:
        return Response(order_serializer.errors, status=400)


@api_view(['GET'])
def get_order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        surcharge_rates = SurchargeRates.objects.first()
        pet_friendly_surcharge = surcharge_rates.pet_friendly_surcharge if surcharge_rates else Decimal("100.00")
        smoking_surcharge = surcharge_rates.smoking_surcharge if surcharge_rates else Decimal("200.00")

        # Calculate days stayed as an integer
        total_cost = Decimal("0.00")
        for booking in order.bookings.all():
            days_stayed = (booking.end_date - booking.start_date).days
            booking_cost = booking.room.room_type.price * days_stayed

            if booking.room.is_pet_friendly:
                booking_cost += pet_friendly_surcharge
            if booking.room.is_smoking:
                booking_cost += smoking_surcharge

            total_cost += booking_cost

        # Update the order's total cost if necessary
        order.total_cost = total_cost
        order.save(update_fields=['total_cost'])

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

@api_view(['POST'])
@transaction.atomic
def mark_order_paid(request):
    order_id = request.data.get('orderID')
    order = get_object_or_404(Order, id=order_id)
    order.is_paid = True
    order.save()

    # Optionally, update any bookings to 'reserved' status if they were 'pending'
    order.bookings.update(status='reserved')

    return Response({'status': 'Order marked as paid'}, status=200)
