from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from utils.authorization import validate
from utils.services import NOTFICATION_SERVICE_URL


# Create your views here.
notification_service_address = os.environ.get('NOTIFICATION_SVC_ADDRESS')
# notification_service_address = NOTFICATION_SERVICE_URL

# Create your views here.
class NotificationMessagesView(APIView):
    def get(self,request,user_id,*args,**kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{notification_service_address}/api/notificationmessages/{user_id}/"
            print(url)
            response = requests.get(url)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
      

class MarkAllUnreadNotificationsAsRead(APIView):
    def post(self, request, user_id, *args, **kwargs):
        payload, err = validate(request)
            
        if payload:
            url = f"http://{notification_service_address}/api/mark-all-unread-notifications-as-read/{user_id}/"
            print(url)
            response = requests.post(url, data=request.data)

            return Response(response.json(), status=response.status_code)   
        else:
            return Response({'error': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
       
