from rest_framework import serializers
from .models import BroadcstNotification

class BroadcstNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcstNotification
        fields = '__all__'

