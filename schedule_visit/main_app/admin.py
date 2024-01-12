
from django.contrib import admin
from .models import AvailableTimes, TimeSlot, ScheduledVisit

admin.site.register(TimeSlot)
admin.site.register(AvailableTimes)
admin.site.register(ScheduledVisit)
