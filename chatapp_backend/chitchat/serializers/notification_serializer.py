from rest_framework import serializers
from chitchat.models import Notification
from chitchat.models import Message


class MessageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    message = MessageContentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
