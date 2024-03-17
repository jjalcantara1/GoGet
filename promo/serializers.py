from rest_framework import serializers
from .models import *

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'
        read_only_fields = ('times_redeemed',)