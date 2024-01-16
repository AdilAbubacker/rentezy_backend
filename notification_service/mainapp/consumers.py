import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name, {"type": "chat.message", "message": message}
    #     )

    # Receive message from room group
    # async def send_notification(self, event):
    #     message = event["message"]
    #     # user_id = event["user_id"]
    #     print('message send')
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         "message": message
    #         # "user_id": user_id
    #     }))

    async def send_notification(self, event):
        id = event['id']
        message = event["message"]
        user_id=event['user_id']
        read=event['read']

        # Send message to WebSocket
        # timestamp = datetime.now().isoformat()
        await self.send(text_data=json.dumps({
            'id':id,
            'message': message,
            'user_id':user_id,
            'read':read,
            # 'timestamp': timestamp 
        }))