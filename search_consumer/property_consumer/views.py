# from django_elasticsearch_dsl_drf.viewsets import DocumentVeiwSet
# from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, CompoundFilterBackend
from .models import *
from .serializers import *
from .documents import *
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.response import Response
from .documents import PropertyDocument
from elasticsearch_dsl.connections import connections
from .docserializer import PropertyDocumentSerializer
from rest_framework import status


# class PropertyDocumentView(DocumentViewSet):
#     document = PropertyDocument
#     serializer_class = PropertyDocumentSerializer

#     filter_backends = [
#         FilteringFilterBackend,
#         CompoundFilterBackend
#     ]

#     search_fields = ('title', 'content')
#     multi_match_search_fields = ('title', 'content')
#     fields_fields = {
#         'title':'title',
#         'content':'content'
#     }



# connections.create_connection(alias='default', hosts=['http://localhost:9200'])

class SearchPropertyView(APIView, LimitOffsetPagination):
    search_document = PropertyDocument
    property_doc_serializer = PropertyDocumentSerializer

    def get(self, request, query):
        try:
            print(2)
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'name',
                    'image',
                    'property_type.type',
                ]
            )
            print(1)
            search = self.search_document.search().query(q)
            response = search.execute()
            for r in response:
                print(r)
            serializer = self.property_doc_serializer(response, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    

        except Exception as e:
            return HttpResponse(e, status=500)