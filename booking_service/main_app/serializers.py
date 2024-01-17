from rest_framework import serializers
from .models import AvailableRooms, Booking

class AvailableRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableRooms
        fields = ['room_id', 'property_name', 'image']

class BookingSerializer(serializers.ModelSerializer):
    room = AvailableRoomsSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
