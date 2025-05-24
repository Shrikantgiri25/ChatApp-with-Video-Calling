from rest_framework import serializers
from chitchat.models.user_models import User
from django.db.models import Q
from chitchat.utils.helpers.enums import UserStatus


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
        ]

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        return user
