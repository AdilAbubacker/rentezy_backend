from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from utils.authorization import validate
from rest_framework import status
from utils.services import AUTH_SERVICE_URL, PROPERTY_SERVICE_URL


class PropertyAdminView(APIView):
    def get(self, request):
        payload, err = validate(request)
            
        if payload and payload["is_admin"]:
            response = requests.get(f"{PROPERTY_SERVICE_URL}/api/admin/properties/")

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class TenantListView(APIView):
    def get(self, request):
        payload, err = validate(request)
            
        if payload and payload["is_admin"]:
            response = requests.get(f"{AUTH_SERVICE_URL}/api/admin/tenants/")

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LandlordListView(APIView):
    def get(self, request):
        payload, err = validate(request)
            
        if payload and payload["is_admin"]:
            response = requests.get(f"{AUTH_SERVICE_URL}/api/admin/landlords/")

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        

class PropertyRequestsView(APIView):
    def get(self, request):
        payload, err = validate(request)
            
        if payload and payload["is_admin"]:
            response = requests.get(f"{PROPERTY_SERVICE_URL}/api/admin/property-requests/")

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
       
    
class ApprovePropertyView(APIView):
    def promote_to_landlord(self, owner_id):
        promote_to_landlord_url = f"{AUTH_SERVICE_URL}/api/admin/promote_to_landlord/{owner_id}/"
        response = requests.post(promote_to_landlord_url)
        return response

    def approve_property(self, property_id):
        approve_property_url = f"{PROPERTY_SERVICE_URL}/api/admin/approve-property/{property_id}/"
        response = requests.post(approve_property_url)
        return response

    def post(self, request, pk):
        payload, err = validate(request)

        if payload and payload["is_admin"]:
            owner_id = request.data['owner_id']
            property_id = pk

            # Promote owner to landlord
            promote_response = self.promote_to_landlord(owner_id)

            # Approve the property
            approve_response = self.approve_property(property_id)

            return Response({
                'promote_response': promote_response.json(),
                'approve_response': approve_response.json()
            }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)