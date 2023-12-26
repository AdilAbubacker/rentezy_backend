from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import PropertyDocument
from .models import Property

class PropertyDocumentSerializer(DocumentSerializer):
    class Meta:
        model = Property 
        document = PropertyDocument

        fields = '__all__'
