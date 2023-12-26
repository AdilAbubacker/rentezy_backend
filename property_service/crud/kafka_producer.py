from django.conf import settings
from confluent_kafka import Producer
import json

class PropertyKafkaProducer:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_SERVER})

    def send_property_data(self, property_data, operation):
        topic = settings.KAFKA_PROPERTY_TOPIC
        key = str(property_data['id'])
        message = json.dumps({
            'operation': operation,
            'data': property_data
        })
        
        self.producer.produce(topic, key=key, value=message)
        self.producer.flush()
