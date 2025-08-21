import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["company_chat"]
messages_collection = db["messages"]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.dept_id = self.scope['url_route']['kwargs']['dept_id']
        self.group_name = f"dept_{self.dept_id}"

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = data.get("sender")
        message = data.get("message")

        # save in MongoDB
        messages_collection.insert_one({
            "dept_id": self.dept_id,
            "sender": sender,
            "message": message
        })

        # broadcast to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "sender": sender,
                "message": message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"]
        }))
