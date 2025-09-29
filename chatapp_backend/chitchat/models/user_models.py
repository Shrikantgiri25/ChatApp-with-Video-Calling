import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from chitchat.manager.user_manager import UserManager
from chitchat.utils.helpers.enums import UserStatus

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    # last_name = models.CharField(max_length=30, null=True, blank=True)
    # username = models.CharField(max_length=30, null=True, blank=True, unique=Trsue)
    email = models.EmailField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    status = models.CharField(
        choices=UserStatus.choices,
        default=UserStatus.NOT_VERIFIED,
        max_length=20,
        null=True,
        blank=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.email}"

    # For saving hashed passwords
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # ADD THESE TWO METHODS
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
