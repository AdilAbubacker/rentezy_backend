from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class BroadcstNotification(models.Model):
    message = models.TextField()
    user_id = models.IntegerField()
    # broadcast_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    read = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ['-broadcast_on']


@receiver(post_save, sender=BroadcstNotification)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        print('signal worked')
        print(instance.id,'idhgidhg')
        channel_layer = get_channel_layer()

        channel_name = f"chat_room_{instance.user_id}"

        async_to_sync(channel_layer.group_send)(
            channel_name,
            {
                'type':'send_notification',
                'id':instance.id,
                'message':instance.message,
                'user_id':instance.user_id,
                # 'broadcast_on':instance.broadcast_on,
                'read':instance.read
            }
        )
        # return HttpResponse("Done")

# # Connect the signal with weak=False to ensure it is not garbage collected
# post_save.connect(notification_handler, sender=BroadcstNotification, weak=False)