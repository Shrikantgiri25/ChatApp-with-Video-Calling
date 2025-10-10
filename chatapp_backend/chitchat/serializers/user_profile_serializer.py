from rest_framework import serializers
from chitchat.models import User, UserProfile
from django.conf import settings


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "bio",
            "is_online",
            "last_seen",
        ]
        read_only_fields = ["is_online", "last_seen"]
    
    def get_profile_picture(self, obj):
        """Return full media URL for profile picture"""
        if obj.profile_picture:
            return f"{settings.MEDIA_URL}{obj.profile_picture}"
        return None

    def update(self, instance, validated_data):
        """Handle profile picture deletion and updates"""
        # Get the profile_picture from the request context
        request = self.context.get('request')
        
        if request and 'profile_picture' in request.FILES:
            # New file uploaded
            instance.profile_picture = request.FILES['profile_picture']
        elif request and request.data.get('profile_picture') == '':
            # Empty string means delete the picture
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
            instance.profile_picture = None
        
        # Update bio
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


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
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        """Update user and profile data"""
        profile_data = validated_data.pop("profile", {})

        # Update User fields
        instance.full_name = validated_data.get("full_name", instance.full_name)
        instance.status = validated_data.get("status", instance.status)
        instance.save(update_fields=["full_name", "status"])

        # Update Profile fields
        if profile_data or self.context.get('request'):
            profile_serializer = self.fields["profile"]
            profile_serializer.context['request'] = self.context.get('request')
            profile_serializer.update(instance.profile, profile_data)

        return instance