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
        profile_data = validated_data.pop("profile", {})

        # Track changed fields for User
        user_fields = []
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                user_fields.append(attr)
        if user_fields:
            instance.save(update_fields=user_fields)

        # Track changed fields for Profile
        profile = instance.profile
        profile_fields = []
        for attr, value in profile_data.items():
            if getattr(profile, attr) != value:
                setattr(profile, attr, value)
                profile_fields.append(attr)
        if profile_fields:
            profile.save(update_fields=profile_fields)

        return instance

