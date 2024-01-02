from django.shortcuts import render, redirect
from rest_framework import generics
from .models import RoomType, Room, Hotel
from .serializers import RoomTypeSerializer, RoomSerializer
from .forms import HotelForm, RoomTypeForm


class RoomTypeList(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')  # Redirect to a success page or home page
    else:
        form = HotelForm()
    return render(request, 'hotel_form.html', {'form': form})


def admin_panel(request):
    # Logic for your admin panel homepage can be added here
    return render(request, 'admin_panel.html')

def add_room_type(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')  # Assuming 'admin-panel' is the named URL pattern for your admin panel homepage
    else:
        form = RoomTypeForm()
    return render(request, 'add_room_type.html', {'form': form})