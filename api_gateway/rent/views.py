from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import requests
import os
from utils.authorization import validate
from utils.services import RENT_SERVICE_URL


# Create your views here.
rent_service_address = os.environ.get('RENT_SVC_ADDRESS')
# rent_service_address = RENT_SERVICE_URL

# Create your views here.
class RentedPropertiesListView(APIView):
    def get(self, request):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{rent_service_address}/api/rented_properties/"
            print(url)
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
class RentPaymentDeatailsView(APIView):
    def get(self, request, rent_id):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{rent_service_address}/api/rented_properties/{rent_id}"
            print(url)
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

class RentPaymentView(APIView):
    def post(self, request):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{rent_service_address}/api/pay_monthly_rent"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
