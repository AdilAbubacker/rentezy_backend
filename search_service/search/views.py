from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.response import Response
from .documents import PropertyDocument
from elasticsearch_dsl.connections import connections
from .docserializers import PropertyDocumentSerializer
from rest_framework import status
from elasticsearch_dsl import Search

# Define the connection parameters
connection_params = {
    'hosts': ['http://localhost:9200'],
    # 'hosts': ['https://elasticsearch-master:9200'],
    # 'verify_certs': False,  # Disable SSL verification
    # 'http_auth': ('elastic', 'randompassword')  # Add HTTP Basic Auth credentials
}

# Create the connection
connections.create_connection(alias='default', **connection_params)

class SearchPropertyView(APIView, LimitOffsetPagination):
    search_document = PropertyDocument
    property_doc_serializer = PropertyDocumentSerializer

    def get(self, request, query):
        q = Q('multi_match',query=query,fields=['name','address','city'], fuzziness='AUTO')
        search = self.search_document.search().query(q)
        response = search.execute()
        for r in response:
            print(r)
        serializer = self.property_doc_serializer(response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # try:
        # except Exception as e:
        #     return HttpResponse(e, status=500)

class GetAllPropertiesView(APIView):
    search_document = PropertyDocument
    property_doc_serializer = PropertyDocumentSerializer

    def get(self, request):

        search_response = self.search_document.search().execute()

        serializer = self.property_doc_serializer(search_response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetPropertyView(APIView):
    search_document = PropertyDocument
    property_doc_serializer = PropertyDocumentSerializer

    def get(self, request, pk):

        property_document = self.search_document.get(id=pk)

        # Serialize the retrieved document
        serializer = self.property_doc_serializer(property_document)
        return Response(serializer.data, status=status.HTTP_200_OK)