from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import reverse
import requests
import os
from utils.authorization import validate
from utils.services import BOOKING_SERVICE_URL

# Create your views here.
booking_service_address = os.environ.get('BOOKING_SVC_ADDRESS')
# booking_service_address = BOOKING_SERVICE_URL

class BookingView(APIView):
    def post(self, request):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{booking_service_address}/api/book/"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)