import json
from confluent_kafka import Consumer, KafkaException
from django.conf import settings
from .serializers import BroadcstNotificationSerializer
from datetime import datetime
from pytz import timezone 

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
                self.process_message(msg.value().decode('utf-8'))

        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()
    

    def process_message(self, data):
        print('proccessing message')
        try:
            message_dict = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return
        
        # message_dict['broadcast_on'] = datetime.now(timezone('UTC'))

        serializer = BroadcstNotificationSerializer(data=message_dict)

        if serializer.is_valid():
            serializer.save()
            print('Notification created: {}'.format(data))
        else:
            print('Invalid data: {}'.format(serializer.errors))