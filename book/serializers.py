from rest_framework import serializers
<<<<<<< HEAD
from .models import Order, Booking
=======
from .models import Order
from adminpanel.models import Booking
>>>>>>> c8ae5a250c2185831e11b9f6969dc96de6146541

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
