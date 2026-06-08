import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer  # ✅ Import this

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.receiver_id = int(self.scope["url_route"]["kwargs"]["receiver_id"])  # ✅ Convert to int

        # ✅ Ensure the user is authenticated
        if not self.user.is_authenticated or self.user.id is None:
            await self.close()
            return
        
        self.room_name = f"chat_{min(self.user.id, self.receiver_id)}_{max(self.user.id, self.receiver_id)}"
        self.room_group_name = f"chat_{self.room_name}"

        # ✅ Join WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()  # ✅ Ensure message is not empty

        if not message:
            return  # ✅ Ignore empty messages

        # ✅ Save message in the database
        await self.save_message(self.user.id, self.receiver_id, message)

        # ✅ Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
            },
        )

    async def chat_message(self, event):
        """ Send the received message to the WebSocket """
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        sender = User.objects.filter(id=sender_id).first()  # ✅ Avoid exceptions
        receiver = User.objects.filter(id=receiver_id).first()

        if sender and receiver:
            Message.objects.create(sender=sender, receiver=receiver, message=message)  # ✅ Save only if both users exist
