from django.db.models import Count, Q
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookingSerializer
from adminpanel.models import RoomType, Booking
from adminpanel.serializers import RoomTypeSerializer
from datetime import datetime


class BookingAPIView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        bookings = Booking.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def available_room_types(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    guest_counts = request.query_params.getlist('guest_count')  # Expecting a list of guest counts

    # Assuming guest_counts is a list of integers like ['2', '3']
    guest_counts = [int(count) for count in guest_counts]

    # Logic to get room types for each guest count
    available_room_types = []
    for count in guest_counts:
        # Filter RoomType based on available rooms and capacity
        room_types = RoomType.objects.filter(
            id__in=[room_type.id for room_type in RoomType.objects.all() if
                    room_type.available_rooms(start_date, end_date, count).exists()]
        )
        serialized = RoomTypeSerializer(room_types, many=True)
        available_room_types.append(serialized.data)

    flat_list = [item for sublist in available_room_types for item in sublist]
    return Response(flat_list)


@api_view(['GET'])
def room_types_availability(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    room_types = RoomType.objects.all().prefetch_related('room_set')
    conflicting_bookings = Booking.objects.filter(
        start_date__lt=end_date,
        end_date__gt=start_date
    )
    booked_room_ids = set(conflicting_bookings.values_list('room_id', flat=True))

    available_room_types = []
    for room_type in room_types:
        # Dictionary to hold the available rooms organized by category
        categories_with_rooms = {
            'standard': {'count': 0, 'availableRoomIds': []},
            'pet_friendly': {'count': 0, 'availableRoomIds': []},
            'smoking_friendly': {'count': 0, 'availableRoomIds': []},
            'both': {'count': 0, 'availableRoomIds': []},
        }

        # Populate the categories_with_rooms dictionary
        for room in room_type.room_set.all():
            if room.id not in booked_room_ids:
                category = 'both' if room.is_pet_friendly and room.is_smoking else (
                    'pet_friendly' if room.is_pet_friendly else (
                        'smoking_friendly' if room.is_smoking else 'standard'
                    )
                )
                categories_with_rooms[category]['count'] += 1
                categories_with_rooms[category]['availableRoomIds'].append(room.id)

        # Use the serialized data which includes the price and other details
        room_type_data = RoomTypeSerializer(room_type).data
        room_type_data['categories'] = categories_with_rooms

        # Add the room type data to the available_room_types list
        available_room_types.append(room_type_data)

    return Response(available_room_types)
