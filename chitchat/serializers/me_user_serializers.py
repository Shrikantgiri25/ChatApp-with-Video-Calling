

from rest_framework import serializers
from chitchat.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "bio",
            "is_online",
            "last_seen",
        ]



class MeUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "status",
            "profile",
        ]
