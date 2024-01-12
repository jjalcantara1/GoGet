from rest_framework import viewsets
from .models import Hotel, RoomType, Room
from .serializers import HotelSerializer, RoomTypeSerializer, RoomSerializer

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
