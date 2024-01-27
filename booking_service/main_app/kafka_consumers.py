import json
from .models import AvailableRooms
from confluent_kafka import Consumer, KafkaException
from django.conf import settings
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
                self.process_message(msg.value())

                    
        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()
    

    def process_message(self, data):
        print('proccessing message')
        try:
            data = json.loads(data)  # Convert the string to a Python dictionary

            operation = data.get('operation')
            
            if operation == 'create':
                # Extract relevant fields from the Kafka data
                room_id = data['data']['id']
                property_name = data['data']['name']
                image = data['data']['image']
                
                # Check if the record already exists in the database
                available_room = AvailableRooms.objects.create(
                            room_id=room_id,
                            property_name=property_name,
                            image=image,
                            price=10000
                        )
                print('Available room created:')

        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
        except KeyError as e:
            print(f'Missing key in data: {e}')
        except Exception as e:
            print(f'Error processing message: {e}')