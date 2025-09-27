from rest_framework import serializers
from chitchat.models import Conversation
from chitchat.serializers.user_serializer import UserSerializer
from chitchat.serializers.group_serializer import GroupSerializer
class ConversationSerializer(serializers.ModelSerializer):
    user_one = UserSerializer(read_only=True)
    user_two = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    last_message = serializers.CharField(read_only=True)
    unread_message_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Conversation
        fields = ["id", "conversation_type", "user_one", "user_two", "group", "created_at", "updated_at", "unread_message_count", "last_message"]
