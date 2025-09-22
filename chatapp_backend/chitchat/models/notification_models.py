import uuid
from django.db import models
from .message_models import Message
from .user_models import User
from .call_models import Call
from chitchat.utils.helpers.choices_fields import NOTIFICATION_TYPE
from django.core.exceptions import ValidationError


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="message_notifications",
        null=True,
        blank=True,
    )
    call = models.ForeignKey(
        Call,
        on_delete=models.CASCADE,
        related_name="call_notifications",
        null=True,
        blank=True,
    )

    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="sent_notifications", null=True
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="notifications", null=True
    )

    # If the user has seen the notification it will be false
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Ensure the notification is linked to either call or message"""
        if not self.message and not self.call:
            self.full_clean()

    def __str__(self):
        return f"{self.notification_type} for {self.recipient.email} from {self.sender.email} at {self.created_at}"
