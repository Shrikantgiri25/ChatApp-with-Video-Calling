import uuid
from django.db import models
from models.user_models import User
from models.group_models import Group
from utils.helpers.choices_fields import CONVERSATION_TYPE


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPE)

    # One to One chat
    user_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversation_initiated",
        null=True,
        blank=True,
    )
    user_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversation_recieved",
        null=True,
        blank=True,
    )

    # Group Chat
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="conversations",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.conversation_type == "private":
            return f"Private chat between {self.user_one.username} and {self.user_two.username}"
        else:
            return f"Group chat: {self.group.name}"
