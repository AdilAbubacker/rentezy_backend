from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class BroadcstNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=BroadcstNotification)
def notification_handler(sender, instance, created, **kwargs):
    print('signal worked')
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_room_3",
        {
            'type':'send_notification',
            'message':"notification"
        }
    )
    # return HttpResponse("Done")