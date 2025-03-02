import uuid
from django.db import models
from chitchat.utils.helpers.file_naming_helper import create_unique_filename
from .user_models import User
from chitchat.utils.helpers.choices_fields import ATTACHMENT_FILE_TYPE
from chitchat.utils.validators.file_validator import validate_file_size


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    messages = models.ManyToManyField(
        "Message", blank=True, related_name="attachments"
    )  # many attchment can belong to one message, one attachment can belong to many message if we forward it.
    content = models.FileField(
        upload_to=create_unique_filename, validators=[validate_file_size]
    )  # We can add custom validators of different type
    content_type = models.CharField(
        max_length=20, choices=ATTACHMENT_FILE_TYPE, default="other"
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content.name} - {self.content_type}"
