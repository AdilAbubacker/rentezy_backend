from django.shortcuts import render
from users.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserSerializer

# Create your views here.
class PromoteToLandlordView(APIView):
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        if not user.is_landlord:
            user.is_landlord = True
            user.save()
            return Response({'message':'promoted to landlord'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message':'Already landlord'}, status=status.HTTP_208_ALREADY_REPORTED)
    
    
class TenantListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_landlord=False, is_admin=False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LandlordListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_landlord=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)