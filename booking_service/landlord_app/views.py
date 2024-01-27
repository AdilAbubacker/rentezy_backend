from django.shortcuts import render
from main_app.models import Booking
from main_app.serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
class BookingListView(APIView):
    AUTH_SERVICES_API_URL = "http://127.0.0.1:8000/api/get_usernames/" 

    def get(self, request):
        print('dfh')
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)

        
        return Response(serializer.data, status=status.HTTP_200_OK)