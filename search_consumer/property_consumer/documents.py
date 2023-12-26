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

# from django_elasticsearch_dsl import Document, fields, Index
# from .models import Property

# PUBLISHER_INDEX = Index('properties')

# PUBLISHER_INDEX.settings(
#     number_of_shards = 1,
#     number_of_replicas = 1
# )

# @PUBLISHER_INDEX.doc_type
# class PropertyDocument(Document):
#     id = fields.IntegerField(attr='id')
#     name = fields.TextField(
#         fields = {
#             "raw" : {
#                 "type": 'keyword'
#             }
#         }
#     )

#     image = fields.TextField(
#         fields = {
#             "raw" : {
#                 "type": 'keyword'
#             }
#         }
#     )

#     class Django(object):
#         model = Property