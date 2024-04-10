import logging
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hotel, RoomType, Room, Booking, SurchargeRates
from .serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer, GuestLogSerializer, \
    SurchargeRatesSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request,*args, **kwargs)

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request,*args, **kwargs)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])  # Set permissions as needed
def get_rooms_by_type(request, room_type_id):
    rooms = Room.objects.filter(room_type__id=room_type_id)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


logger = logging.getLogger(__name__)


@api_view(['POST'])
def add_room(request):
    logger.info(f"Received data for new room: {request.data}")

    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        errors = serializer.errors
        logger.error(f"Error when trying to create a room: {errors}")
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# @permission_classes([permissions.IsAuthenticated])  # Set permissions as needed
def edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    serializer = RoomSerializer(room, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @permission_classes([permissions.IsAuthenticated])  # Set permissions as needed
def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    room.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        # ...

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def get_available_rooms(request, room_type_id, start_date, end_date):
        # Perform your date validation and conversion here as needed
        room_type = get_object_or_404(RoomType, id=room_type_id)
        available_rooms = room_type.available_rooms(start_date, end_date)
        available_room_ids = list(available_rooms.values_list('id', flat=True))
        return Response(available_room_ids)

@api_view(['GET'])
def guest_log(request):
    # You can add filtering by date range if needed
    bookings = Booking.objects.all()
    serializer = GuestLogSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_surcharge_rates(request):
    rates = SurchargeRates.objects.first()
    if rates:
        return Response({
            'pet_friendly_surcharge': rates.pet_friendly_surcharge,
            'smoking_surcharge': rates.smoking_surcharge
        })
    return Response({'error': 'Surcharge rates not found'}, status=404)

@api_view(['PUT'])
def update_surcharge_rates(request):
    rates = SurchargeRates.objects.first()
    serializer = SurchargeRatesSerializer(rates, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)