from rest_framework import viewsets, status
from rest_framework.response import Response
from .kafka_producer import PropertyKafkaProducer
from .serializers import PropertySerializer
from .models import Property
from rest_framework.parsers import MultiPartParser, FormParser


class PropertyViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request): # api/properties post
        print(request.data)
        serializer = PropertySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            kafka_producer = PropertyKafkaProducer()
            kafka_producer.send_property_data(serializer.data, operation='create')
            print('done sending')
        except Exception as e:
            print(f"Error sending data to Kafka: {str(e)}")
            return Response({"error": 'error_message'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED) 
    

    def list(self, request):# api/properties/<str:id> get
        owner_id = request.GET.get('owner_id')
        properties = Property.objects.filter(owner_id=owner_id)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):# api/properties/<str:id> get
        property = Property.objects.get(id=pk)
        owner_id = request.GET.get('owner_id')

        if str(property.owner_id) == str(owner_id):
            serializer = PropertySerializer(property)
            return Response(serializer.data)
        else:
            return Response('not authorized', 401)


    def update(self, request, pk=None):# api/properties/<str:id> put
        property = Property.objects.get(id=pk)
        owner_id = request.GET.get('owner_id')

        if str(property.owner_id) == str(owner_id):
            print(request.data)
            serializer = PropertySerializer(instance=property, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            try:
                kafka_producer = PropertyKafkaProducer()
                kafka_producer.send_property_data(serializer.data, operation='update')
                print('done sending')
            except Exception as e:
                print(f"Error sending data to Kafka: {str(e)}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('not authorized', 401)


    def destroy(self, request, pk=None):# api/properties/<str:id> delete
        property = Property.objects.get(id=pk)
        owner_id = request.GET.get('owner_id')

        if str(property.owner_id) == str(owner_id):
            property.delete()
            try:
                kafka_producer = PropertyKafkaProducer()
                kafka_producer.send_property_data({"id":pk}, operation='delete')
                print('done sending')
            except Exception as e:
                print(f"Error sending data to Kafka: {str(e)}")
            return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            print('hi')
            return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)