from django.shortcuts import render
from rest_framework.views import APIView
from crud.models import Property
from crud.serializers import PropertySerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class PropertyAdminView(APIView):
    def get(self, request):
        properties = Property.objects.filter(status='Approved')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
    
class PropertyRequestsView(APIView):
    def get(self, request):
        properties = Property.objects.filter(status='Pending')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
    

class ApprovePropertyView(APIView):
    def post(self, request, pk):
        property = Property.objects.filter(id=pk).first()
        if property:
            property.status = 'Approved'
            property.save()
            return Response({'message':'property approved'}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({'message':'item not found'}, status=status.HTTP_404_NOT_FOUND)

class PropertyListView(APIView):
    def get(self, request):
        properties = Property.objects.filter(status='Approved')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)