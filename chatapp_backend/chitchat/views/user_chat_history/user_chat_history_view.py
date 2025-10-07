from rest_framework.views import APIView
from rest_framework import permissions, throttling, status
from django.db.models import Q
import logging

from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.pagination import Pagination
from chitchat.models.user_conversation_metadata import UserConversationMetadata
from chitchat.serializers.user_conversation_metadata_serializer import UserConversationMetadataSerializer

logger = logging.getLogger(__name__)


class UserChatHistoryView(APIView):
    """
    Returns the user's personalized conversation list,
    using UserConversationMetadata for efficient unread tracking.
    """
    serializer_class = UserConversationMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = Pagination

    def get(self, request):
        user = request.user
        logger.info(f"Fetching chat history for user: {user.email}")

        try:
            # Step 1: Apply search if provided
            search_query = request.query_params.get("search", "").strip()

            queryset = (
                UserConversationMetadata.objects
                .select_related(
                    "conversation",
                    "conversation__user_one",
                    "conversation__user_two",
                    "conversation__group",
                    "last_message_sender",
                )
                .filter(user=user)
                .order_by("-last_message_timestamp", "-updated_at")
            )

            # Step 2: Apply search filters (on other user email or group name)
            if search_query:
                queryset = queryset.filter(
                    Q(conversation__user_one__email__icontains=search_query)
                    | Q(conversation__user_two__email__icontains=search_query)
                    | Q(conversation__group__group_name__icontains=search_query)
                )

            # Step 3: Paginate
            paginator = self.pagination_class()
            page_queryset = paginator.paginate_queryset(queryset, request)

            # Step 4: Serialize
            serializer = self.serializer_class(page_queryset, many=True, context={"request": request})

            logger.info(f"Chat history fetched successfully for user: {user.email}")
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.exception(f"Error fetching chat history for user: {user.email}")
            return create_api_response(
                message="Something went wrong while fetching chat history.",
                errors={"details": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
