from django.core.management.base import BaseCommand
from property_consumer.kafka_consumer import KafkaConsumer
from django.conf import settings

class Command(BaseCommand):
    help = 'Consume messages from Kafka'

    def handle(self, *args, **options):
        kafka_consumer = KafkaConsumer(
            group_id=settings.KAFKA_GROUP_ID,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            topic=settings.KAFKA_TOPIC
        )

        kafka_consumer.consume_messages()