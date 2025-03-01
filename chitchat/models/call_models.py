import uuid
from django.db import models
from .user_models import User
from .conversation_models import Conversation
from .group_models import Group
from utils.helpers.choices_fields import CALL_TYPE, CALL_STATUSES
from django.core.exceptions import ValidationError


class Call(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Linking to conversation
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="calls",
    )

    caller = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="initiated_calls"
    )
    # One on One and Group Call support
    participants = models.ManyToManyField(
        User, blank=True, related_name="group_call_participants"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="group_calls",
    )

    call_type = models.CharField(max_length=20, choices=CALL_TYPE)
    status = models.CharField(max_length=20, choices=CALL_STATUSES, default="ongoing")

    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    is_missed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.conversation.group:
            if self.participants.exists() < 2:
                raise ValidationError("A group call must have atleast 2 participants")
        else:
            if self.participants.exists() != 2:
                raise ValidationError("An One on One call must have exactly 2 participants")
        return super().clean()

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        if self.started_at and self.ended_at:
            self.duration = int((self.ended_at - self.started_at).total_seconds())
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        if self.group:
            return f"{self.call_type} group call in {self.group.group_name} | {self.status}"
        return f"{self.call_type} call from {self.caller.username} to {self.conversation.user_two.username} | {self.status}"
