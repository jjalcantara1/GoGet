from django.db import models
from adminpanel.models import Booking

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact_no = models.CharField(max_length=100)
    start_date = Booking.start_date
    end_date = Booking.end_date


# Create your models here.
