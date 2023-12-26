from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Message


class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChatMessagesView(APIView):
    def get(self,request,tenant_id,landlord_id,*args,**kwargs):

        # Fetch all messages related to the user and doctor
        messages=Message.objects.filter(
            (models.Q(sender=tenant_id)&models.Q(receiver=landlord_id)) |
            (models.Q(sender=landlord_id)&models.Q(receiver=tenant_id))
        ).order_by('timestamp')

        serializer=MessageSerializer(messages,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)