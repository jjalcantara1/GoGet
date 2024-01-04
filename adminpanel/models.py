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
    total_rooms = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_smoking = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_type.name} - Room {self.number}"
