import uuid
from django.db import models
from models.user_models import User
from models.conversation_models import Conversation
from models.attachment_models import Attachment
from models.group_models import Group


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(editable=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_messages",
    )

    attachment = models.ManyToManyField(Attachment, blank=True, related_name="messages")
    is_deleted = models.BooleanField(default=False)
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replies"
    )

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
