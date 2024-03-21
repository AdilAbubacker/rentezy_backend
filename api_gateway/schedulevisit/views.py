from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from django.utils import timezone
import requests
import os
from utils.authorization import validate
from utils.services import SHEDULEVISIT_SERVICE_URL

schedulevisit_service_address = os.environ.get('SHEDULEVISIT_SVC_ADDRESS')
# schedulevisit_service_address = SHEDULEVISIT_SERVICE_URL


class AvailableTimesAndDatesView(APIView):
    def get(self, request, room_id):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{schedulevisit_service_address}/api/dates_and_times/{room_id}"
            print(url)
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


class AvailableTimesCreateView(APIView):
    def post(self, request, *args, **kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{schedulevisit_service_address}/api/available_times/create//"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

class ScheduleVisitView(APIView):
    def post(self, request):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{schedulevisit_service_address}/api/rented_properties/"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class TenantScheduledVisits(APIView):
    def get(self, request, tenant_id):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{schedulevisit_service_address}/api/scheduled_visits/{tenant_id}"
            print(url)
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
       