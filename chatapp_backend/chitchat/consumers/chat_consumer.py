from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from chitchat.models import Message
from chitchat.models.group_models import Group
from chitchat.models.user_models import User
from chitchat.models.conversation_models import Conversation
from chitchat.models.attachment_models import Attachment
from chitchat.models.user_conversation_metadata import UserConversationMetadata
from django.db.models import Q
from chitchat.utils.helpers.choices_fields import CONVERSATION_TYPE
from chitchat.serializers.message_serializer import MessageSerializer
from chitchat.serializers.notification_serializer import NotificationSerializer
from chitchat.utils.user_status.redis_user_status import is_user_online
from chitchat.consumers.sanitize_groupnames import (
    sanitize_group_name,
    sanitize_notification_group_name,
)
from asgiref.sync import sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer handles WebSocket connections for chat rooms.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        if "room_name" in self.scope["url_route"]["kwargs"]:
            raw_room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_name = sanitize_group_name(raw_room_name)
        elif "group_id" in self.scope["url_route"]["kwargs"]:
            self.room_name = self.scope["url_route"]["kwargs"]["group_id"]
        else:
            await self.close()
            return

        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        
        # Reset unread count when user opens conversation
        await self.reset_unread_count_for_user()
        
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
            
        saved_message, receiver, group = await self.save_message(
            content, sender, receiver, group_id, attachment_ids, reply_to
        )
        
        if saved_message is None:
            return
        
        # Update metadata for all participants
        await self.update_user_conversation_metadata(saved_message, sender, receiver, group)
        
        send_data = await self.serialize_message(saved_message)
        
        if send_data:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {
                        "message_obj": str(send_data["message_obj"]),
                        "timestamp": send_data["timestamp"],
                    },
                },
            )
            
            if send_data["message_obj"]["conversation"]["conversation_type"] == "group":
                notifications = await self.create_group_message_notifications(
                    saved_message, sender, group
                )

                # Send notification to all members except sender
                for notif, member_id in notifications:
                    if is_user_online(member_id):
                        await self.channel_layer.group_send(
                            f"notifications_user_{member_id}",
                            {
                                "type": "send.notification",
                                "notification": {
                                    "id": str(notif["id"]),
                                    "type": "message",
                                    "group": group.group_name,
                                    "sender": sender.email,
                                    "message": saved_message.content,
                                    "created_at": str(notif["created_at"]),
                                },
                            },
                        )
                        await self.mark_message_delivered(saved_message.id)
            else:
                notification = await self.create_message_notification(
                    saved_message, sender, receiver
                )
                group_name = (
                    f"notifications_user_{sanitize_notification_group_name(receiver)}"
                )
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "send.notification",
                        "notification": {
                            "id": str(notification["id"]),
                            "type": "message",
                            "sender": sender.email,
                            "message": saved_message.content,
                            "created_at": str(notification["created_at"]),
                        },
                    },
                )
                await self.mark_message_delivered(saved_message.id)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @sync_to_async
    def update_user_conversation_metadata(self, message, sender, receiver, group):
        """
        Update or create UserConversationMetadata for all participants.
        - Updates last message info for everyone
        - Increments unread count only for recipients (not sender)
        """
        conversation = message.conversation
        timestamp = message.created_at
        content = message.content
        
        if conversation.conversation_type == "private":
            # For private chat - create/update for both users
            for user in [conversation.user_one, conversation.user_two]:
                if user:
                    metadata, created = UserConversationMetadata.objects.get_or_create(
                        conversation=conversation,
                        user=user
                    )
                    
                    # Update last message info for both
                    metadata.last_message_content = content
                    metadata.last_message_sender = sender
                    metadata.last_message_timestamp = timestamp
                    
                    # Increment unread count only for the receiver
                    if user != sender:
                        metadata.unread_message_count += 1
                    
                    metadata.save()
        
        elif conversation.conversation_type == "groups" and group:
            # For group chat - create/update for all members
            group_members = group.members.all()
            
            for member in group_members:
                metadata, created = UserConversationMetadata.objects.get_or_create(
                    conversation=conversation,
                    user=member
                )
                
                # Update last message info for everyone
                metadata.last_message_content = content
                metadata.last_message_sender = sender
                metadata.last_message_timestamp = timestamp
                
                # Increment unread count only for members who didn't send the message
                if member != sender:
                    metadata.unread_message_count += 1
                
                metadata.save()

    @sync_to_async
    def reset_unread_count_for_user(self):
        """
        Reset unread count to 0 when user opens the conversation.
        """
        try:
            # Try to find the conversation by room_name
            conversation = None
            
            # For group chats, room_name is the group_id
            if self.room_name:
                conversation = Conversation.objects.filter(
                    Q(id=self.room_name) | Q(group__id=self.room_name)
                ).first()
                
                # For private chats, need to find by participants
                if not conversation:
                    # room_name might be sanitized user IDs
                    conversation = Conversation.objects.filter(
                        Q(user_one=self.user) | Q(user_two=self.user),
                        conversation_type="private"
                    ).first()
            
            if conversation:
                metadata = UserConversationMetadata.objects.filter(
                    conversation=conversation,
                    user=self.user
                ).first()
                
                if metadata:
                    metadata.unread_message_count = 0
                    metadata.last_read_at = timezone.now()
                    metadata.save(update_fields=['unread_message_count', 'last_read_at', 'updated_at'])
        except Exception as e:
            # Silent fail - don't break connection
            pass

    async def save_message(
        self, content, sender, receiver, group, attachment_ids, reply_to
    ):
        """
        Save the message to the database.
        """
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
                return None, None, None
                
        if group:
            receiver = None
            try:
                group = await database_sync_to_async(Group.objects.get)(id=group)
                ismember = await database_sync_to_async(group.is_member)(sender)
                group_admin_id = await database_sync_to_async(
                    lambda: group.group_admin.id
                )()
                if not ismember and group_admin_id != sender.id:
                    await self.send(
                        json.dumps({"error": "User is not part of the group."})
                    )
                    return None, None, None
                conversation = await self.get_group_conversation(group=group)
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
                return None, None, None
        elif receiver:
            group = None
            try:
                receiver = await database_sync_to_async(User.objects.get)(id=receiver)
            except User.DoesNotExist:
                await self.send(json.dumps({"error": "User does not exist."}))
                return None, None, None
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
            return None, None, None
        return message, receiver, group

    @sync_to_async
    def mark_message_delivered(self, message_id):
        from chitchat.models import Message
        try:
            Message.objects.filter(id=message_id).update(is_delivered=True)
        except Message.DoesNotExist:
            pass

    @database_sync_to_async
    def serialize_message(self, message):
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
        
        # Create conversation and metadata for both users
        conversation = Conversation.objects.create(
            user_one=sender,
            user_two=receiver,
            conversation_type=CONVERSATION_TYPE[0][0],
        )
        
        # Create metadata for both users
        UserConversationMetadata.objects.create(
            conversation=conversation,
            user=sender
        )
        UserConversationMetadata.objects.create(
            conversation=conversation,
            user=receiver
        )
        
        return conversation

    @database_sync_to_async
    def get_group_conversation(self, group):
        conversation = Conversation.objects.filter(
            group=group,
            conversation_type=CONVERSATION_TYPE[1][0],
        ).first()
        if conversation:
            return conversation
        
        # Create conversation
        conversation = Conversation.objects.create(
            group=group,
            conversation_type=CONVERSATION_TYPE[1][0],
        )
        
        # Create metadata for all group members
        for member in group.members.all():
            UserConversationMetadata.objects.create(
                conversation=conversation,
                user=member
            )
        
        return conversation

    @database_sync_to_async
    def create_message_notification(self, message, sender, recipient):
        from chitchat.models import Notification

        notification_instance = Notification.objects.create(
            notification_type="message",
            message=message,
            sender=sender,
            recipient=recipient,
        )
        return NotificationSerializer(notification_instance).data

    async def create_group_message_notifications(self, message, sender, group):
        notifications = []
        group_members = await self.get_group_members_excluding_sender(group, sender)

        for member in group_members:
            notification = await self.create_message_notification(
                message, sender, member
            )
            notifications.append((notification, member.id))
        return notifications

    @database_sync_to_async
    def get_group_members_excluding_sender(self, group, sender):
        return list(group.members.exclude(id=sender.id))

    @database_sync_to_async
    def get_group_by_id(self, group_id):
        return Group.objects.prefetch_related("members").get(id=group_id)