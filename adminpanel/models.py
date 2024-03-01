from django.db import models


# Create your models here.

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

    # In your RoomType model
    # In your RoomType model
    def available_rooms(self, check_in, check_out):
        # Get all rooms of this type
        all_rooms = self.room_set.all()

        # Get IDs of booked rooms in the range
        booked_room_ids = Booking.objects.filter(
            room__in=all_rooms,
            start_date__lt=check_out,
            end_date__gt=check_in
        ).values_list('room', flat=True)

        # Now get available rooms by excluding the booked ones
        available_rooms = all_rooms.exclude(id__in=booked_room_ids)
        return available_rooms


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_smoking = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_type.name} - Room {self.number}"

    pass

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking for {self.room} from {self.start_date} to {self.end_date}"
