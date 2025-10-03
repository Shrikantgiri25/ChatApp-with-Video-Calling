from rest_framework import serializers
from django.conf import settings
from chitchat.models import User

class UserListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    bio = serializers.CharField(source="profile.bio", read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "profile_picture",
            "bio"
        ]
    
    def get_profile_picture(self, obj):
        """
        Returns the full URL for the profile picture or None if not set.
        """
        try:
            if obj.profile and obj.profile.profile_picture:
                # Return full URL with MEDIA_URL prepended
                return f"{settings.MEDIA_URL}{obj.profile.profile_picture}"
        except User.profile.RelatedObjectDoesNotExist:
            pass
        return None