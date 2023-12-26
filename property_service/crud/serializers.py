from rest_framework import serializers
from .models import Property, Amenity, PropertyAmenity
from rest_framework import serializers



class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'



# class RoomAmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RoomAmenity
#         fields = '__all__'


# class PropertyImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PropertyImages
#         fields = '__all__'

# class PropertySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Property
#         fields = '__all__'

# class AmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Amenity
#         fields = '__all__'

# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'

# class PropertyAmenitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PropertyAmenity
#         fields = '__all__'

# class PropertySerializer(serializers.ModelSerializer):
#     rooms = RoomSerializer(many=True, read_only=True)
#     amenities = AmenitySerializer(many=True, read_only=True)
#     bookings = BookingSerializer(many=True, read_only=True)
#     property_amenities = PropertyAmenitySerializer(many=True, read_only=True)

#     class Meta:
#         model = Property
#         fields = '__all__'


# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'
