from chitchat.serializers.user_registration_serializers import (
    UserRegistrationSerializer,
)
from chitchat.models.user_models import User
from rest_framework.exceptions import ValidationError


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
                raise ValidationError("Account with email already exists.")
        except Exception as e:
            raise Exception(
                [f"Failed to Create user for email: {data.get('email')}"]
            ) from e
