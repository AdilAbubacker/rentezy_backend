from django.contrib import admin
from .models import AvailableRooms, Booking

# Register your models here.
admin.site.register(AvailableRooms)
admin.site.register(Booking)