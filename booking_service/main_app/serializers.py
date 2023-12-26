from rest_framework import serializers
from .models import AvailableRooms, Booking

class AvailableRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableRooms
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
