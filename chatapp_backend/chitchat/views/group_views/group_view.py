from rest_framework.views import APIView
from rest_framework import permissions, throttling, status
from rest_framework.exceptions import Throttled
import logging
from django.db import transaction

from chitchat.models import Conversation, UserConversationMetadata, Message, Notification
from chitchat.serializers.group_serializer import GroupSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.choices_fields import CONVERSATION_TYPE
from chitchat.utils.helpers.constants import (
    TO_MANY_REQUEST_429,
    SOMETHING_WENT_WRONG,
    GROUP_CREATED,
)

logger = logging.getLogger(__name__)


class GroupView(APIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def post(self, request):
        try:
            group_admin = request.user
            group_data = request.data.copy()
            group_data["group_admin"] = group_admin.id  # Use ID in serializer
            group_data["members"].append(group_admin.id)
            serializer = self.serializer_class(data=group_data)
            if not serializer.is_valid():
                return create_api_response(
                    message="Validation failed",
                    errors=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                # Save group
                group = serializer.save()
                members = list(group.members.all())

                # Create group conversation
                conversation, _ = Conversation.objects.get_or_create(
                    user_one=group_admin,
                    group=group,
                    conversation_type=CONVERSATION_TYPE[1][0],
                )

                # Create system message
                member_content = f"{group_admin} added you"
                admin_content = f"Created the group '{group.group_name}'"
                message = Message.objects.create(
                    sender=group_admin,
                    content=member_content,
                    conversation=conversation,
                    group=group,
                )
                timestamp = message.created_at

                # Prepare bulk UserConversationMetadata
                metadata_objects = []
                for member in members:
                    if member.email == group_admin.email:
                        metadata_objects.append(
                            UserConversationMetadata(
                                conversation=conversation,
                                user=group_admin,
                                last_message_content=admin_content,
                                last_message_sender=group_admin,
                                last_message_timestamp=timestamp,
                                unread_message_count=0,
                            )
                        )
                    else:
                        metadata_objects.append(
                            UserConversationMetadata(
                                conversation=conversation,
                                user=member,
                                last_message_content=member_content,
                                last_message_sender=group_admin,
                                last_message_timestamp=timestamp,
                                unread_message_count=1,
                            )
                        )
                UserConversationMetadata.objects.bulk_create(metadata_objects)
                # Create notifications in bulk
                notification_objects = [
                    Notification(
                        notification_type="message",
                        message=message,
                        sender=group_admin,
                        recipient=member,
                    )
                    for member in members if member != group_admin
                ]
                Notification.objects.bulk_create(notification_objects)

            logger.info(f"Group '{group.group_name}' created successfully by {group_admin}")
            return create_api_response(
                message=GROUP_CREATED,
                data={"group": GroupSerializer(group).data},
                http_status=status.HTTP_201_CREATED,
            )

        except Throttled as e:
            logger.warning(f"Request throttled: {e}")
            return create_api_response(
                message=TO_MANY_REQUEST_429,
                http_status=status.HTTP_429_TOO_MANY_REQUESTS,
                errors=str(e),
            )

        except Exception as e:
            logger.exception(f"Unexpected error in Group creation: {e}")
            return create_api_response(
                message=SOMETHING_WENT_WRONG,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )
