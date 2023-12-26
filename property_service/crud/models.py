from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('bed', 'Bed'),
        ('room', 'Room'),
        ('house', 'House'),
    ]

    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    name = models.CharField(max_length=255)
    owner_id = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='House')
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    description = models.TextField()
    image = models.ImageField(upload_to='property/', null=True, blank=True)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    number_of_bathrooms = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def save(self, *args, **kwargs):
        self.name = f'{self.number_of_rooms}BHK {self.property_type} for rent at {self.city}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property_type} at {self.name}"
    


class Amenity(models.Model):
    amenity_name = models.CharField(max_length=255)


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)


# class Room(models.Model):
#     quantity = models.IntegerField(null=True, blank=True)
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_active = models.BooleanField(default=True)

# class Locality(models.Model):
# class RoomAmenity(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)


# class PropertyImages(models.Model):
#     image = models.ImageField(upload_to='property_images/')
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Variant: {self.property} - Image: {self.image.name}"