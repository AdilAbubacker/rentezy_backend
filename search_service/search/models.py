from django.db import models

# Create your models here.
class Property(models.Model):
    PROPERTY_TYPES = [
        ('bed', 'Bed'),
        ('room', 'Room'),
        ('house', 'House'),
    ]
    id = models.IntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=255)
    owner_id = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    description = models.TextField()
    image = models.CharField(max_length=255)
    number_of_rooms = models.IntegerField(blank=True, null=True)
    number_of_bathrooms = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)