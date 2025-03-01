import uuid
from django.db import models
from models.user_models import User
from utils.helpers.file_naming_helper import create_unique_filename


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=30, null=False, unique=True)
    group_avatar = models.ImageField(
        upload_to=create_unique_filename, null=True, blank=True
    )
    description = models.CharField(max_length=50, null=True, blank=True)
    group_admin = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="groups"
    )
    members = models.ManyToManyField(User, blank=True, related_name="groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
