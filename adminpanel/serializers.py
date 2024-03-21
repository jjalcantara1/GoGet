from rest_framework import serializers
from .models import Hotel, RoomType, Room

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def update(self, instance, validated_data):
        # Check if 'image' key is present in the validated_data
        image = validated_data.pop('image', None)
        if image is not None:
            instance.image = image
        else:
            # If no image is provided, we remove the image field from the validated_data
            validated_data.pop('image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RoomTypeSerializer(serializers.ModelSerializer):
    is_pet_friendly = serializers.SerializerMethodField()
    is_smoking = serializers.SerializerMethodField()

    class Meta:
        model = RoomType
        fields = '__all__'

    def update(self, instance, validated_data):
        # Check if 'image' key is present in the validated_data
        image = validated_data.pop('image', None)
        if image is not None:
            instance.image = image
        else:
            # If no image is provided, we remove the image field from the validated_data
            validated_data.pop('image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_is_pet_friendly(self, obj):
        return obj.has_pet_friendly()

    def get_is_smoking(self, obj):
        return obj.has_smoking_room()

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'is_available', 'is_smoking', 'is_pet_friendly']

