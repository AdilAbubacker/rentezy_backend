from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import reverse
import requests  # Assuming you have requests installed
import os

class SearchPropertyView(APIView):
    def get(self, request, query):
        search_url = reverse('search-property', kwargs={'query': query})
        search_service_address = os.environ.get('SEARCH_SVC_ADDRESS')
        search_service_response = requests.get(f"http://{search_service_address}/{search_url}")
        return Response(search_service_response.json(), status=search_service_response.status_code)

class GetAllPropertiesView(APIView):
    def get(self, request):
        properties_url = reverse('get-all-properties')
        search_service_address = os.environ.get('SEARCH_SVC_ADDRESS')
        properties_service_response = requests.get(f"http://{search_service_address}/{properties_url}")
        return Response(properties_service_response.json(), status=properties_service_response.status_code)

class GetPropertyView(APIView):
    def get(self, request, pk):
        property_url = reverse('get-property', kwargs={'pk': pk})
        search_service_address = os.environ.get('SEARCH_SVC_ADDRESS')
        property_service_response = requests.get(f"http://{search_service_address}/{property_url}")
        return Response(property_service_response.json(), status=property_service_response.status_code)
