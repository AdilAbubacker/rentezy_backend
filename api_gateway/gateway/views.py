from django.http import HttpResponseBadRequest
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterUserView(APIView):
    def post(self, request):
        if request.method == 'POST':
            auth_service_url = "http://127.0.0.1:8000/api/register/"

            response = requests.post(auth_service_url, data=request.data)

            return Response(response.json(), status=response.status_code)
    

class LoginView(APIView):
    def post(self, request):
        auth_service_url = "http://127.0.0.1:8000/api/login/"

        response = requests.post(auth_service_url, data=request.data)

        if response.status_code == 201 or response.status_code == 200:
            auth_response = response.json()
            token = auth_response.get('jwt', None)

            if token:
                # Include the entire payload from auth service in the response
                response = Response(auth_response)
                response.set_cookie(key='jwt', value=token, httponly=True)
                print(response.data)
                return response

        elif response.status_code == 401:
            response_data = response.json()
            return Response(response_data, status=response.status_code)
        else:
            return Response({'message': 'Login failed'}, status=response.status_code)
        
class UserView(APIView):
    def get(self, request):
        auth_service_url = "http://127.0.0.1:8000/api/user/"

        response = requests.get(auth_service_url, data=request.data)

        return Response(response.json(), status=response.status_code)
        
        
class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response 
    
    