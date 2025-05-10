import uuid
from django.db import models
from .user_models import User
from chitchat.utils.helpers.constants import (
    USER_EMAIL_VERIFICATION,
    SET_PASSWORD,
)
from django.utils import timezone
class IssuedToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issued_tokens",
    )
    token = models.CharField(max_length=1024, unique=True)
    purpose = models.CharField(max_length=50, choices=[(USER_EMAIL_VERIFICATION, "Email Verification"), (SET_PASSWORD, "Password Reset")])
    issued_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # You can deactivate/expire manually

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        return f"IssuedToken to {self.user.email} for {self.purpose}"