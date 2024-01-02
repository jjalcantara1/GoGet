from django import forms
from .models import Hotel, RoomType, Room


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'
