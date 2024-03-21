from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import reverse
import requests
import os
from utils.authorization import validate
from utils.services import CHAT_SERVICE_URL

# Create your views here.
chat_service_address = os.environ.get('CHAT_SVC_ADDRESS')
# chat_service_address = CHAT_SERVICE_URL

class MessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{chat_service_address}/chat/create/"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    

class ChatMessagesView(APIView):
    def get(self,request,tenant_id,landlord_id,*args,**kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{chat_service_address}/chat/chatmessages/{tenant_id}/{landlord_id}/"
            
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


class UsersChattedWithView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{chat_service_address}/chat/users_chatted_with/{user_id}/"
            
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)