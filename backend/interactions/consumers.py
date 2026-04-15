import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from django.db.models import F

from .models import Conversation, Message, ConversationUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"
        self.user = self.scope["user"]

        # validar usuario autenticado
        if self.user.is_anonymous:
            await self.close()
            return

        # marcar usuario como online
        await sync_to_async(self.set_online)(True)

        # unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # enviar evento "online" al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "username": self.user.username,
                "online": True
            }
        )


    async def disconnect(self, close_code):

        # marcar usuario como offline
        await sync_to_async(self.set_online)(False)

        #  enviar evento "offline"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_status",
                "username": self.user.username,
                "online": False
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        #  TYPING INDICATOR
        if "typing" in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_event",
                    "typing": data["typing"],
                    "username": self.user.username
                }
            )
            return

        #  EVENTO DE LECTURA (✓✓ visto)
        if data.get("read"):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_read",
                    "username": self.user.username
                }
            )
            return

        #  MENSAJE NORMAL
        message = data.get("message", "")

        msg = await self.save_message(self.user.id, message)

        # aumentar unread_count a otros usuarios
        await sync_to_async(self.increment_unread)(self.user.id)

        # reenviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.text,
                "image_url": None,
                "username": msg.sender.username
            }
        )


    #  "escribiendo"
    async def typing_event(self, event):
        await self.send(text_data=json.dumps({
            "typing": event["typing"],
            "username": event["username"]
        }))


    #  MENSAJE A TODOS
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "image_url": event["image_url"],
            "username": event["username"]
        }))


    #  ✓✓ VISTO
    async def message_read(self, event):
        await self.send(text_data=json.dumps({
            "read": True,
            "username": event["username"]
        }))


    #  ONLINE / OFFLINE
    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            "status": True,
            "username": event["username"],
            "online": event["online"]
        }))


    # FUNCIONES AUXILIARES

    @sync_to_async
    def save_message(self, user_id, text):

        conversation = Conversation.objects.get(id=self.conversation_id)

        if not conversation.users.filter(id=user_id).exists():
            raise Exception("Usuario no pertenece a esta conversación")

        user = User.objects.get(id=user_id)

        return Message.objects.create(
            conversation=conversation,
            sender=user,
            text=text
        )


    @sync_to_async
    def increment_unread(self, sender_id):
        ConversationUser.objects.filter(
            conversation_id=self.conversation_id
        ).exclude(
            user_id=sender_id
        ).update(
            unread_count=F("unread_count") + 1
        )


    def set_online(self, status):
        profile = self.user.profile
        profile.is_online = status
        profile.save()
