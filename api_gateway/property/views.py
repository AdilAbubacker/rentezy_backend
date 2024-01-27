import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from utils.authorization import validate


class PropertyGatewayView(APIView):
    property_service_url = "http://127.0.0.1:8002/api/properties/"

    def get(self, request):
        payload, err = validate(request)
            
        if payload:
            user_id = payload.get('id')

            params = {'owner_id': user_id}

            response = requests.get(self.property_service_url, params=params)

            return Response(response.json(), status=response.status_code)
        else:
            return Response({'error': 'not authorized'}, 401)


    def post(self, request):
        payload, err = validate(request)

        if payload:
            user_id = payload.get('id')
            request.data['owner_id'] = user_id

            # Extract file from request.data
            files = {'image': request.data['image']}

            # Remove the 'image' key from request.data to avoid treating it as a file
            request.data.pop('image', None)

            response = requests.post(self.property_service_url, data=request.data, files=files)

            return Response(response.json(), status=response.status_code)
        else:
            return Response({'error': 'not authorized'}, 401)


class PropertyGatewayPKView(APIView):
    property_service_url = "http://127.0.0.1:8002/api/properties/{pk}"

    def get(self, request, pk):
        payload, err = validate(request)

        if payload and payload["is_landlord"]:
            user_id = payload.get('id')
            
            params = {'owner_id': user_id}
        
            url = self.property_service_url.format(pk=pk)

            response = requests.get(url, params=params)

            return Response(response.json(), status=response.status_code)
        else:
            return Response({'error': 'not authorized'}, 401)

    

    def put(self, request, pk):
        payload, err = validate(request)

        if payload and payload["is_landlord"]:
            user_id = payload.get('id')
            #getting ownerid and adding to the json data to save it on db
            request.data['owner_id'] = user_id

            params = {'owner_id': user_id}

            url = self.property_service_url.format(pk=pk)

            files = {'image': request.data['image']}
            request.data.pop('image', None)

            response = requests.put(url, data=request.data, files=files, params=params)

            return Response(response.json(), status=response.status_code)
        else:
            return Response({'error': 'not authorized'}, 401)

    

    def delete(self, request, pk):
        payload, err = validate(request)

        if payload and payload["is_landlord"]:
            user_id = payload.get('id')

            params = {'owner_id':user_id}

            url = self.property_service_url.format(pk=pk)

            response = requests.delete(url, params=params)
            print(response)

            return Response(response, status=response.status_code)
        else:
            return Response({'error': 'not authorized'}, 401)