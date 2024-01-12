from confluent_kafka import Consumer, KafkaException
from django.conf import settings

class KafkaConsumer:
    def __init__(self, topic):
        self.topic = topic
        self.consumer = Consumer(settings.KAFKA_CONFIG)

    def consume_messages(self):
        self.consumer.subscribe([self.topic])

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        print(f"Error: {msg.error()}")
                        break

                # Process the received message
                print(f"Received message from topic '{msg.topic()}' partition {msg.partition()}: {msg.value().decode('utf-8')}")

        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()