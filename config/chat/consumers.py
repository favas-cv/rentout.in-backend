
# 1. DRF → create room → room_id

# 2. User connects:
#    ws://chat/1/

# 3. connect():
#    → get room_id
#    → create group name
#    → channel_name auto-created
#    → join group

# 4. receive():
#    → get message from client
#    → group_send()

# 5. group_send():
#    → sends to ALL channel_names in group

# 6. chat_message():
#    → each user gets message

# 7. self.send():
#    → message sent to frontend

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from channels.db import database_sync_to_async
from accounts.models import User
from notification.services import create_notification
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):  #startwhen the router url hit,
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        
        self.room_group_name = f"chat_{self.room_id}"
        
        user = self.scope.get('user') 
        # user = await self.get_test_user() #for testing 
        
        # security layer1
        
        if not user or not user.is_authenticated:
            await self.close(code=4001) #unauthorized
            return
        
        # security layer2
        is_participent = await self.check_participent(user,self.room_id)
        if not is_participent:
            await self.close(code=4003) #forbiden
            return 
         
        
        # joingropu
        
            # channel_name	one user connection
            # group_name	chat room
            # channel_layer	message system (Redis)
        self.user = user
        await self.channel_layer.group_add( #this will join the groupname with ur channel name
            self.room_group_name,
            self.channel_name #everyone has diffrent by tab or phone like
        )
        await self.accept() #server say connection apporoved ypu are inside goup
        
    async def disconnect(self, close_code): # call when close tab or network fail
        await self.channel_layer.group_discard( # our chanel is removed from group others will there 
            self.room_group_name, 
            self.channel_name
        )
        
    
    async def receive(self, text_data):

        data = json.loads(text_data)

        event_type = data.get('type', 'message')

        user = self.user

        # ---------------- SEEN EVENT ----------------

        if event_type == 'seen':

            message_id = data.get('message_id')

            if not message_id:
                return

            await self.mark_message_seen(message_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_seen',
                    'message_id': message_id
                }
            )

            return

        # ---------------- NORMAL MESSAGE ----------------

        message = data.get('message')

        if not message:
            return

        saved_message = await self.save_message(
            user,
            self.room_id,
            message
        )

        await self.send_message_notification(saved_message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'timestamp': str(saved_message.timestamp),
                'msg_id': saved_message.id,
            }
        )
        
    async def chat_message(self, event):
        await self.mark_as_delivered(event['msg_id'])

        await self.send(text_data=json.dumps({
            'type': 'message',           # ← add type so frontend can distinguish
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
            'msg_id': event['msg_id'],
            'is_delivered': True,        # ← frontend shows ✓
            'is_read': False,            # ← frontend shows ✓✓ only after seen event
        })) 
        
    async def message_seen(self, event):

        await self.send(text_data=json.dumps({
            'type': 'seen',
            'message_id': event['message_id']
        }))
    
    
    


    @database_sync_to_async
    def mark_message_seen(self, message_id):
        msg = Message.objects.get(id=message_id)
        if self.user != msg.sender:
            msg.is_read = True          # ← was is_seen (doesn't exist in your DB)
            msg.read_at = timezone.now() # ← was seen_at (doesn't exist in your DB)
            msg.save()
    
    
    
    @database_sync_to_async
    def mark_as_delivered(self, msg_id):
        msg = Message.objects.get(id=msg_id)
        # Only the receiver should trigger delivered, not the sender themselves
        if self.user != msg.sender:
            msg.is_delivered = True
            msg.save()
    
    
    
    @database_sync_to_async
    def check_participent(self,user,room_id):
        return ChatRoom.objects.filter(
            id=room_id,
            participants=user
        ).exists()
    
       

        
    @database_sync_to_async  # orm is sync but webscket is aync so in there stuck for that use this , so sync will use another thread poll
    def save_message(self,user,room_id,content):
        
        room = ChatRoom.objects.get(id = room_id)
        return Message.objects.create(
            room=room,
            sender=user,
            content=content
        )
    
    @database_sync_to_async
    def send_message_notification(self, message_obj):

        room = message_obj.room

        receiver = room.participants.exclude(
            id=message_obj.sender.id
        ).first()

        create_notification(
            sender=message_obj.sender,
            receiver=receiver,
            notification_type='MESSAGE',
            title='New Message',
            message=message_obj.content,
            redirect_url='/chat/'
        )
        

