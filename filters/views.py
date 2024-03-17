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
