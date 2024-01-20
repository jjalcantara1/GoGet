from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer
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

@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])  # Set permissions as needed
def add_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

