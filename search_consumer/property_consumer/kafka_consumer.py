import json
from confluent_kafka import Consumer, KafkaError
from .serializers import PropertySerializer
from .models import Property

class KafkaConsumer:
    def __init__(self, group_id, bootstrap_servers, topic):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.topic = topic
        self.consumer.subscribe([topic])

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                
                print('Received message: {}'.format(msg.value().decode('utf-8')))
                self.process_message(msg.value())
                
        finally:
            self.consumer.close()

    def process_message(self, message):
        try:
            data = json.loads(message)
            operation = data.get('operation')
            if operation == 'create':
                self.handle_create(data['data'])
            elif operation == 'update':
                self.handle_update(data['data'])
            elif operation == 'delete':
                self.handle_delete(data['data'])
            else:
                print(f"Unknown operation: {operation}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    def handle_create(self, data):
        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Created: {}'.format(data))
        else:
            print('Invalid data: {}'.format(serializer.errors))

    def handle_update(self, data):
        property = Property.objects.get(id=data['id'])
        serializer = PropertySerializer(instance=property, data=data)
        if serializer.is_valid():
            serializer.save()
            print('Updated: {}'.format(data))
        else:
            print('Invalid data: {}'.format(serializer.errors))

    def handle_delete(self, data):
        property = Property.objects.get(id=data['id'])
        property.delete()
        print(f"Handling delete operation with data: {data}")