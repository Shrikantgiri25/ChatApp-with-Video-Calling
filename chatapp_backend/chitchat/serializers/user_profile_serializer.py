from rest_framework import serializers
from chitchat.models import User, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "bio",
            "is_online",
            "last_seen",
        ]
        read_only_fields = ["is_online", "last_seen"]  # Keep these readonly if needed


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "status",
            "profile",
        ]
        read_only_fields = [
            "email"
        ]  # Optional: Make email read-only if it shouldn't change

    def update(self, instance, validated_data):
        # Extract profile data
        profile_data = validated_data.pop("profile", {})

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related UserProfile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance
