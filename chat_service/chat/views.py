from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Message
import requests  

class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChatMessagesView(APIView):
    def get(self,request,tenant_id,landlord_id,*args,**kwargs):
        print('kkk')
        # Fetch all messages related to the user and doctor
        messages=Message.objects.filter(
            (models.Q(sender=tenant_id)&models.Q(receiver=landlord_id)) |
            (models.Q(sender=landlord_id)&models.Q(receiver=tenant_id))
        ).order_by('timestamp')

        serializer=MessageSerializer(messages,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UsersChattedWithView(APIView):
    AUTH_SERVICES_API_URL = "http://127.0.0.1:8000/api/get_usernames/" 

    def get(self, request, user_id, *args, **kwargs):

        # Retrieve distinct combinations of sender and receiver IDs from Message model
        users_chatted_with = Message.objects.filter(
            models.Q(sender=user_id) | models.Q(receiver=user_id)
        ).values('sender', 'receiver').distinct()

        # Extract unique user IDs from the combinations
        user_ids = set()
        for chat in users_chatted_with:
            user_ids.add(chat['sender'])
            user_ids.add(chat['receiver'])

        # Remove the current user's ID from the set
        user_ids.discard(user_id)

        try:
            response = requests.get(self.AUTH_SERVICES_API_URL, params={'user_ids': list(user_ids)})
            response.raise_for_status()
            user_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(user_data, status=status.HTTP_200_OK)