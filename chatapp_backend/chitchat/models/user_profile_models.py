import os
import uuid
from django.db import models
from .user_models import User
from chitchat.utils.helpers.file_naming_helper import create_unique_filename
from django.conf import settings


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

    # def save(self, *args, **kwargs):
    #     if self.id:
    #         try:
    #             user_instace = UserProfile.objects.get(id=self.id)
    #             if (
    #                 user_instace.profile_picture
    #                 and user_instace.profile_picture != self.profile_picture
    #             ):
    #                 old_picture_path = os.path.join(
    #                     settings.MEDIA_ROOT, user_instace.profile_picture.name
    #                 )
    #                 if os.path.exists(old_picture_path):
    #                     os.remove(old_picture_path)
    #         except User.DoesNotExist:
    #             pass
    #     return super().save(*args, **kwargs)
