from datetime import datetime

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from book.models import Order

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
    contact_no = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    features = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    


    def __str__(self):
        return self.name

    def available_rooms(self, start_date, end_date, guest_count=1):
        guest_count = int(guest_count)  # Ensure guest_count is an integer

        # If room type capacity is less than guest count, return no rooms
        if self.capacity < guest_count:
            return self.room_set.none()

        # Get all rooms of this type that are not booked during the requested dates
        booked_room_ids = Booking.objects.filter(
            room__room_type=self,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).values_list('room', flat=True)

        available_rooms = self.room_set.exclude(id__in=booked_room_ids)
        return available_rooms

    def has_pet_friendly(self):
        return self.room_set.filter(is_available=True, is_pet_friendly=True).exists()

    def has_smoking_room(self):
        return self.room_set.filter(is_available=True, is_smoking=True).exists()


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_smoking = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_type.name} - Room {self.number}"

    pass
def create_default_order():
    order, _ = Order.objects.get_or_create(name='Default', email='default@example.com', contact_no='1234567890', created_at='2022-01-01 00:00:00')
    return order.id

class Booking(models.Model):
    STATUS_CHOICES = (
        ('reserved', 'Reserved'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('pending', 'Pending'),
        # Add more status choices as needed
    )

    order = models.ForeignKey(Order, related_name='bookings', on_delete=models.CASCADE, default=create_default_order)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')



    def __str__(self):
        return f"Booking for {self.room} from {self.start_date} to {self.end_date}"
