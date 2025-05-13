from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from chitchat.models import Message
from chitchat.models.group_models import Group
from chitchat.models.user_models import User
from chitchat.models.conversation_models import Conversation
from chitchat.models.attachment_models import Attachment
from django.db.models import Q
from chitchat.utils.helpers.choices_fields import CONVERSATION_TYPE
from chitchat.serializers.message_serializer import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer handles WebSocket connections for chat rooms.
    It allows users to join chat rooms, send messages, and receive messages.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON"}))
            return
        content = data.get("content", None)
        attachment_ids = data.get("attachment_ids", [])
        sender = self.scope["user"]
        receiver = data.get("receiver", None)
        group_id = data.get("group_id", None)
        reply_to = data.get("reply_to", None)
        if not content and not attachment_ids:
            await self.send(
                json.dumps({"error": "Cannot send empty message and attachment."})
            )
            return
        saved_message = await self.save_message(
            content, sender, receiver, group_id, attachment_ids, reply_to
        )
        if saved_message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {
                        "message_obj": saved_message["message_obj"],
                        "timestamp": saved_message["timestamp"],
                    },
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def save_message(
        self, content, sender, receiver, group_id, attachment_ids, reply_to
    ):
        """
        Save the message to the database.
        """
        # If the message is sent to group
        attachment_obj = []
        reply_to_obj = None
        if attachment_ids:
            attachment_obj = await self.get_all_attachments(attachment_ids)
        if reply_to:
            reply_to_obj = await self.get_replied_to_message(reply_to)
            if not reply_to_obj:
                await self.send(
                    json.dumps({"error": "Message which you replies was not found."})
                )
                return
        if group_id:
            try:
                group = await database_sync_to_async(Group.objects.get)(id=group_id)
                ismember = await database_sync_to_async(group.is_member)(sender)
                if not ismember:
                    await self.send(
                        json.dumps({"error": "User is not part of the group."})
                    )
                    return
                conversation = await database_sync_to_async(Conversation.objects.get)(
                    group=group
                )
                message = await database_sync_to_async(Message.objects.create)(
                    content=content,
                    sender=sender,
                    group=group,
                    conversation=conversation,
                    reply_to=reply_to_obj,
                )
                await database_sync_to_async(message.attachment.set)(attachment_obj)
            except Group.DoesNotExist:
                await self.send(json.dumps({"error": "Group does not exist."}))
                return
        elif receiver:
            try:
                receiver = await database_sync_to_async(User.objects.get)(id=receiver)
            except User.DoesNotExist:
                await self.send(json.dumps({"error": "User does not exist."}))
                return
            conversation = await self.get_private_conversation(sender, receiver)
            message = await database_sync_to_async(Message.objects.create)(
                content=content,
                sender=sender,
                conversation=conversation,
                reply_to=reply_to_obj,
            )
            await database_sync_to_async(message.attachment.set)(attachment_obj)
        else:
            await self.send(
                json.dumps({"error": "No group or user id's were provided"})
            )
            return
        return {
            "message_obj": MessageSerializer(message).data,
            "timestamp": message.created_at.isoformat(),
        }

    @database_sync_to_async
    def get_all_attachments(self, attachment_ids):
        return list(Attachment.objects.filter(id__in=attachment_ids, is_deleted=False))

    @database_sync_to_async
    def get_replied_to_message(self, reply_to):
        try:
            return Message.objects.get(id=reply_to)
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def get_private_conversation(self, sender, receiver):
        conversation = Conversation.objects.filter(
            Q(user_one=sender, user_two=receiver)
            | Q(user_one=receiver, user_two=sender),
            conversation_type=CONVERSATION_TYPE[0][0],
        ).first()
        if conversation:
            return conversation
        return Conversation.objects.create(
            user_one=sender,
            user_two=receiver,
            conversation_type=CONVERSATION_TYPE[0][0],
        )
