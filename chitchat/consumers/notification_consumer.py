# consumers/notification_consumer.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chitchat.models import Notification
from channels.db import database_sync_to_async
from chitchat.utils.user_status.redis_user_status import (
    mark_user_online,
    mark_user_offline,
)
from chitchat.serializers.notification_serializer import NotificationSerializer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.user = self.scope["user"]
        self.group_name = f"notifications_user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        mark_user_online(self.user.id)

        # Send unread notifications
        unread_notifications = await self.get_unread_notifications()
        serializer_notification = await self.serialize_message(unread_notifications)
        await self.send_json(
            {
                "type": "unread_notifications",
                "notifications": str(serializer_notification),
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        mark_user_offline(self.user.id)

    @database_sync_to_async
    def get_unread_notifications(self):
        return list(Notification.objects.filter(recipient=self.user, is_read=False))

    async def send_notification(self, event):
        await self.send_json(
            {"type": "new_notification", "notification": event["notification"]}
        )

    async def receive_json(self, content):
        if content["type"] == "mark_as_read":
            await self.mark_notification_as_read(content["notification_id"])

    @database_sync_to_async
    def mark_notification_as_read(self, notif_id):
        Notification.objects.filter(id=notif_id, recipient=self.user).update(
            is_read=True
        )

    @database_sync_to_async
    def serialize_message(self, notification):
        return NotificationSerializer(notification, many=True).data
