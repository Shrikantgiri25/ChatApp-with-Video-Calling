import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(AbstractBaseUser, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    username = models.CharField(max_length=30, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.email}"

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        if self.password and not self.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2")
        ):
            self.password = make_password(self.password)
        return super().save(force_insert, force_update, using, update_fields)
