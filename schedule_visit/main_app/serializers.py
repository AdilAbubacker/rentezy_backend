# serializers.py
from rest_framework import serializers
from .models import AvailableTimes, TimeSlot, ScheduledVisit

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['time']

class AvailableTimesSerializer(serializers.ModelSerializer):
    times = TimeSlotSerializer(many=True)

    class Meta:
        model = AvailableTimes
        fields = ['room_id', 'times']

class ScheduledVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledVisit
        fields = ['room', 'time_slot', 'visitor_id', 'visit_date']
