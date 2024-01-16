from confluent_kafka import Producer
from django.conf import settings


class KafkaProducer:
    def __init__(self) -> None:
        self.producer = Producer(settings.KAFKA_CONFIG)

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce_message(self, message, topic):
        self.producer.produce(topic, value=message, callback=self.delivery_report)
        self.producer.flush()


# Create a global instance of KafkaProducer
kafka_producer = KafkaProducer()