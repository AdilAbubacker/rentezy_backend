# chat/views.py
from django.http import HttpResponse
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from .models import BroadcstNotification
from .serializers import BroadcstNotificationSerializer
from rest_framework.response import Response
from rest_framework import status

def index(request):
    return render(request, "mainapp/index.html")

def room(request, room_name):
    return render(request, "mainapp/room.html", {"room_name": room_name})

def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_room_3",
        {
            'type':'send_notification',
            'message':"Notification"
        }
    )
    return HttpResponse("Done")

class NotificationMessagesView(APIView):
    def get(self,request,user_id,*args,**kwargs):

        # Fetch all messages related to the user
        messages=BroadcstNotification.objects.filter(user_id=user_id).order_by('-id')[:10]

        # Calculate the count of unread notifications
        unread_count = BroadcstNotification.objects.filter(user_id=user_id, read=False).count()

        serializer=BroadcstNotificationSerializer(messages,many=True)

        response_data = {
            'unread_count': unread_count,
            'messages': serializer.data,
        }

        return Response(response_data,status=status.HTTP_200_OK)
    

class MarkAllUnreadNotificationsAsRead(APIView):
    def post(self, request, user_id, *args, **kwargs):
        unread_notifications = BroadcstNotification.objects.filter(user_id=user_id, read=False)

        for notification in unread_notifications:
            notification.read = True
            notification.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)
