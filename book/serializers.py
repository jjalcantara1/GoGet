from rest_framework import serializers

from filters.serializers import BookingSerializer
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

