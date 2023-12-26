from django.contrib import admin
from .models import Property, Amenity, PropertyAmenity

# Register your models here.
admin.site.register(Property)
admin.site.register(Amenity)
admin.site.register(PropertyAmenity)