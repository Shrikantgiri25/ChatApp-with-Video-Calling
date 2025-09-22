from chitchat.serializers.user_registration_serializers import (
    UserRegistrationSerializer,
)
from chitchat.models.user_models import User
from rest_framework.exceptions import ValidationError
from chitchat.serializers.user_serializer import UserSerializer
from chitchat.utils.helpers.enums import UserStatus


class UserService:
    def create_user(data):
        try:
            user_instance = User.objects.filter(email=data.get("email")).first()
            if not user_instance:
                serializer = UserRegistrationSerializer(data=data)
                if serializer.is_valid():
                    user = serializer.save()
                    return user
                else:
                    raise ValidationError(serializer.errors)
            else:
                if user_instance.status == UserStatus.NOT_VERIFIED:
                    return user_instance
                raise ValidationError("Account with email already exists.")
        except Exception as e:
            raise Exception(
                [f"Failed to Create user for email: {data.get('email')}"]
            ) from e

    def update_user(data):
        try:
            user_email = data.get("email")
            if not user_email:
                raise ValidationError("Email is required to update user.")
            user_instance = User.objects.filter(email=user_email).first()
            if not user_instance:
                raise ValidationError("User with this email does not exist.")
            if user_instance.status == "ACTIVE":
                raise ValidationError("User account is already active.")
            serializer = UserSerializer(user_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.validated_data["status"] = UserStatus.NEW_USER
                serializer.validated_data["is_active"] = True
                user = serializer.save()
                return user
            else:
                raise ValidationError(serializer.errors)
        except Exception as e:
            raise Exception(
                [f"Failed to Add user details for email: {data.get('email')}"]
            ) from e
