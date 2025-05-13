import os
import uuid
from django.db import models
from .user_models import User
from chitchat.utils.helpers.file_naming_helper import create_unique_filename


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=create_unique_filename, null=True, blank=True, max_length=500
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_online = models.BooleanField(default=False)
    bio = models.TextField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}"
