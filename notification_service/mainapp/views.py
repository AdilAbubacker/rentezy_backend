# chat/views.py
from django.http import HttpResponse
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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