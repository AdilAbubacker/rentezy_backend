from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            )
        print('room created',self.room_group_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )
        print('room dosconnected',self.room_group_name)


    # Receive message from WebSocket
    async def receive(self, text_data): 
        print('message recieved', text_data)

        try:
            text_data_json = json.loads(text_data)
            sender = text_data_json.get('sender')
            message_content = text_data_json["message_content"]
            receiver = text_data_json.get('receiver')

            if sender and receiver and message_content:
                message = {
                    'message_content': message_content,
                    'sender': sender,
                    'receiver': receiver
                }

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name, 
                    {
                        "type": "chat.message", 
                        "message_content": message_content,
                        "sender": sender,
                        "receiver": receiver
                    },
                )
                print(message)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message_content"]
        sender=event['sender']
        receiver=event['receiver']

        # Send message to WebSocket
        timestamp = datetime.now().isoformat()
        await self.send(text_data=json.dumps({
            'message_content': message,
            'sender':sender,
            'receiver':receiver,
            'timestamp': timestamp 
        }))