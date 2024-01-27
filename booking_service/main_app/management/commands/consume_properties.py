from django.core.management.base import BaseCommand
from main_app.kafka_consumers import KafkaConsumer

class Command(BaseCommand):
    help = 'Run Kafka consumer'

    def handle(self, *args, **options):
        topic = 'property_topic'
        consumer = KafkaConsumer(topic)
        consumer.consume_messages()