import uuid
from django.db import models
from .user_models import User
from django.conf import settings
from chitchat.utils.helpers.file_naming_helper import create_unique_filename
import os


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=30, null=False, unique=True)
    group_avatar = models.ImageField(
        upload_to=create_unique_filename, null=True, blank=True
    )
    description = models.CharField(max_length=50, null=True, blank=True)
    group_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="admin_of_groups", null=True
    )
    members = models.ManyToManyField(User, blank=True, related_name="groupsmembers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.group_name}"

    def is_member(self, user):
        return self.members.filter(id=user.id).exists()

    def save(self, *args, **kwargs):
        # Delete Old Photo before saving new
        if self.id:
            try:
                old_instance = Group.objects.get(id=self.id)
                if (
                    old_instance.group_avatar
                    and self.group_avatar != old_instance.group_avatar
                ):
                    old_photo_path = os.path.join(
                        settings.MEDIA_ROOT, old_instance.group_avatar.name
                    )
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
            except Group.DoesNotExist:
                pass
        return super().save(*args, **kwargs)
