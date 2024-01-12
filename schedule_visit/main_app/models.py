from django.db import models
from datetime import datetime

class AvailableTimes(models.Model):
    room_id = models.IntegerField(unique=True)
    times = models.ManyToManyField('TimeSlot', related_name='available_times')

class TimeSlot(models.Model):
    time = models.CharField(max_length=8, unique=True)

class ScheduledVisit(models.Model):
    room = models.ForeignKey(AvailableTimes, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    visitor_id = models.IntegerField()
    visit_date = models.DateField()
    title = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Format time as '02:00 PM'
        formatted_time = datetime.strptime(self.time_slot.time, "%I:%M %p").strftime("%I:%M %p")

        # Format date as 'Friday, 5th Jan 2024'
        formatted_date = self.visit_date.strftime("%A, %dth %b %Y")

        # Generate the title
        self.title = f"{formatted_time}, {formatted_date} in Taliparamba"
        
        super().save(*args, **kwargs)

