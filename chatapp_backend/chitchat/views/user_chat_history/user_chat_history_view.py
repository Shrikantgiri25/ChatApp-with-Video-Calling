from rest_framework.views import APIView
from chitchat.serializers.conversation_serializer import ConversationSerializer
from rest_framework import permissions, throttling, status
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.models import Conversation, Message
from django.db.models import Q
import logging
from chitchat.utils.helpers.pagination import Pagination

logger = logging.getLogger(__name__)


class UserChatHistoryView(APIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = Pagination

    def get(self, request):
        # TODO:

        # Add last_message and last_message_sender fields to Conversation model.
        # Create ConversationUnreadCount model to store per-user unread message counts.
        # Use post_save signal on Message to update Conversation last message fields and increment unread counts for other users.
        # Update chat API to read these cached fields instead of querying Message table.
        user_id = request.user.pk
        logger.info(f"Request came for fetching chat history of user: {user_id}")
        try:
            # Get all conversations for this user
            conversations = Conversation.objects.filter(
                Q(user_one__id=user_id) |
                Q(user_two__id=user_id) |
                Q(group__members__id=user_id)
            ).select_related("user_one", "user_two", "group") \
             .prefetch_related("group__members") \
             .order_by("-updated_at")

            # 2️⃣ Paginate first
            paginator = self.pagination_class()
            page_conversations = paginator.paginate_queryset(conversations, request)

            # 3️⃣ Annotate unread count and last message per conversation in page
            conversation_ids = [conv.id for conv in page_conversations]

            messages = Message.objects.filter(conversation_id__in=conversation_ids)

            unread_counts = {}
            last_messages = {}
            last_senders = {}

            for conv_id in conversation_ids:
                conv_messages = messages.filter(conversation_id=conv_id)
                unread_counts[conv_id] = conv_messages.filter(is_read=False).exclude(sender_id=user_id).count()
                last_message_obj = conv_messages.order_by("-created_at").first()
                if last_message_obj:
                    last_messages[conv_id] = last_message_obj.content
                    last_senders[conv_id] = last_message_obj.sender.email
                else:
                    last_messages[conv_id] = None
                    last_senders[conv_id] = None

            # Attach these values to conversation objects for serializer
            for conv in page_conversations:
                conv.unread_message_count = unread_counts.get(conv.id, 0)
                conv.last_message = last_messages.get(conv.id)
                conv.last_message_sender = last_senders.get(conv.id)

            serializer = self.serializer_class(page_conversations, many=True)
            logger.info(f"Fetched chat history of user: {user_id}")
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.exception(f"Error fetching chat history for user: {user_id}")
            return create_api_response(
                message="Something went wrong",
                errors={"details": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
