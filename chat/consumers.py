import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage

class ChatConsumer(WebsocketConsumer):

    def connect(self,projectname):
        self.room_name = str(projectname)
        self.room_group_name = self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def showmessage(self,storemessage):
        #show message 
        for old in storemessage:
            message = old
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message
            }
        )
    
    def receive(self, text_data):
       
        json_text = json.loads(text_data)
        message = json_text["message"]
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message
            }
        )


    def save_messages_to_database(self, messages):
        # Save messages to the database
        for message in messages:
            ChatMessage.objects.create(user=self.scope['user'], content=message)
    
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))