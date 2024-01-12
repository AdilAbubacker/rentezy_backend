from django.core.management.base import BaseCommand
from mainapp.kafka_consumers import KafkaConsumer

class Command(BaseCommand):
    help = 'Run Kafka consumer'

    def handle(self, *args, **options):
        topic = 'notifications'
        consumer = KafkaConsumer(topic)
        consumer.consume_messages()
