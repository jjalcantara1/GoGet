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

    try:
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(hour=14, minute=0)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=12, minute=0)

        # Get all RoomTypes
        room_types = RoomType.objects.all()
        available_room_types = []

        for room_type in room_types:
            if room_type.available_rooms(start_date, end_date).exists():
                available_room_types.append(room_type)

        serializer = RoomTypeSerializer(available_room_types, many=True)
        return Response(serializer.data)
    except ValueError as e:
        # Handle the exception
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

