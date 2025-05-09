from django.db import models


class UserStatus(models.TextChoices):
    NOT_VERIFIED = "NOT_VERIFIED", "Not Verified"
    VERIFIED = "VERIFIED", "Verified"
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"