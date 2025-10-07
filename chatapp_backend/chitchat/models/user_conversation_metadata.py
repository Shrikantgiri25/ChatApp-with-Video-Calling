import uuid
from django.db import models
from .user_models import User
from .conversation_models import Conversation


class UserConversationMetadata(models.Model):
    """
    Stores per-user metadata for conversations.
    Each user gets their own metadata record for each conversation they're part of.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to conversation and user
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="user_metadata"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversation_metadata"
    )
    
    # Last message info (what the user sees in their chat list)
    last_message_content = models.TextField(blank=True, null=True)
    last_message_sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_last_messages"
    )
    last_message_timestamp = models.DateTimeField(null=True, blank=True)
    
    # Unread tracking
    unread_message_count = models.PositiveIntegerField(default=0)
    
    # Additional useful fields
    is_archived = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('conversation', 'user')
        ordering = ['-last_message_timestamp', '-updated_at']
        indexes = [
            models.Index(fields=['user', '-last_message_timestamp']),
            models.Index(fields=['user', 'is_archived', '-last_message_timestamp']),
            models.Index(fields=['conversation', 'user']),
        ]
        verbose_name = "User Conversation Metadata"
        verbose_name_plural = "User Conversation Metadata"

    def __str__(self):
        return f"{self.user.email} - {self.conversation}"
    
    def reset_unread_count(self):
        """Reset unread count to 0"""
        self.unread_message_count = 0
        self.last_read_at = models.functions.Now()
        self.save(update_fields=['unread_message_count', 'last_read_at', 'updated_at'])