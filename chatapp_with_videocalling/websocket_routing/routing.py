from django.urls import re_path
from chitchat.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    # One-to-one chat: uuid1_uuid2
    re_path(r"ws/chat/(?P<room_name>[0-9a-f-]+_[0-9a-f-]+)/$", ChatConsumer.as_asgi()),
    # Group chat: group_uuid
    re_path(r"ws/chat/group_(?P<group_id>[0-9a-f-]+)/$", ChatConsumer.as_asgi()),
    re_path(
        r"ws/notifications/user_(?P<user_id>[0-9a-f-]+)/$",
        NotificationConsumer.as_asgi(),
    ),
]
