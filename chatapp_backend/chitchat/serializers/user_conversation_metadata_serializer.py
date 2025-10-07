from rest_framework import serializers
from chitchat.models.user_conversation_metadata import UserConversationMetadata
from chitchat.models.conversation_models import Conversation
from django.conf import settings


class UserConversationMetadataSerializer(serializers.ModelSerializer):
    """
    Serializer for user's chat list - shows their personalized view of conversations
    """
    conversation_id = serializers.UUIDField(source='conversation.id', read_only=True)
    conversation_type = serializers.CharField(source='conversation.conversation_type', read_only=True)
    
    # For private chats - show the other user's info
    other_user = serializers.SerializerMethodField()
    
    # For group chats - show group info
    group = serializers.SerializerMethodField()
    
    # Last message details
    last_message_sender_email = serializers.CharField(
        source='last_message_sender.email', 
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = UserConversationMetadata
        fields = [
            'id',
            'conversation_id',
            'conversation_type',
            'other_user',
            'group',
            'last_message_content',
            'last_message_sender_email',
            'last_message_timestamp',
            'unread_message_count',
            'is_archived',
            'is_pinned',
            'is_muted',
            'last_read_at',
            'updated_at',
        ]
    
    def get_other_user(self, obj):
        """
        For private chats, return the OTHER user's info (not the current user)
        """
        if obj.conversation.conversation_type != "private":
            return None
        
        request = self.context.get('request')
        current_user = request.user if request else obj.user
        
        # Determine which user is the "other" user
        other_user = None
        if obj.conversation.user_one == current_user:
            other_user = obj.conversation.user_two
        else:
            other_user = obj.conversation.user_one
        
        if not other_user:
            return None
        
        # Build profile picture URL
        profile_picture = None
        if hasattr(other_user, 'profile') and other_user.profile and other_user.profile.profile_picture:
            profile_picture = f"{settings.MEDIA_URL}{other_user.profile.profile_picture}"
        
        # Build bio
        bio = ""
        if hasattr(other_user, 'profile') and other_user.profile:
            bio = other_user.profile.bio or ""
        
        return {
            "id": str(other_user.id),
            "email": other_user.email,
            "profile_picture": profile_picture,
            "bio": bio,
        }
    
    def get_group(self, obj):
        """
        For group chats, return group info
        """
        if obj.conversation.conversation_type != "group":
            return None
        
        group = obj.conversation.group
        if not group:
            return None
        
        group_avatar = None
        if group.group_avatar:
            group_avatar = f"{settings.MEDIA_URL}{group.group_avatar}"
        
        return {
            "id": str(group.id),
            "group_name": group.group_name,
            "group_avatar": group_avatar,
            "description": group.description,
        }