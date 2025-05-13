from rest_framework import serializers
from chitchat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "content",
            "conversation",
            "group",
            "timestamp",
            "is_read",
            "attachment",
            "reply_to",
            "is_deleted",
        ]
        read_only_fields = ["sender", "created_at"]

    def validate(self, attrs):
        # Prevent sender change
        if "sender" in attrs:
            raise serializers.ValidationError(
                "You cannot change the sender of a message."
            )

        # Content or attachment check
        if not attrs.get("content") and not attrs.get("attachment"):
            raise serializers.ValidationError(
                "Message must have either content or attachment."
            )

        # Validate conversation vs group
        conversation = attrs.get("conversation")
        group = attrs.get("group")

        if conversation and group:
            raise serializers.ValidationError(
                "Message cannot be linked to both a conversation and a group."
            )
        if not conversation and not group:
            raise serializers.ValidationError(
                "Message must be linked to either a conversation or a group."
            )

        return attrs
