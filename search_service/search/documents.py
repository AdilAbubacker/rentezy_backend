from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Property


@registry.register_document
class PropertyDocument(Document):

    property_type = fields.ObjectField(
        properties={
            'type': fields.TextField(),
        }
    )

    class Index:
        name = 'properties'

    class Django:
        model = Property
        fields = [
            "id",
            "name",
            "image",
            "owner_id",
            "description",
            "number_of_rooms",
            "number_of_bathrooms",
            "address",
            "city",
            "state"
            ]