import os
import uuid
from django.db import models
from models.user_models import User
from utils.helpers import create_unique_filename


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=create_unique_filename, null=True, blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    status = models.BooleanField(default=False)
    bio = models.TextField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_name}"
