from rest_framework.views import APIView
from chitchat.serializers.conversation_serializer import ConversationSerializer
from rest_framework import permissions, throttling, status
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.models import Conversation, Message
from django.db.models import Q, Count, OuterRef, Subquery
import logging
from chitchat.utils.helpers.pagination import ChatHistoryPagination
logger = logging.getLogger(__name__)


class UserChatHistoryView(APIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = ChatHistoryPagination

    def get(self, request):
        user_id = request.user.pk
        logger.info(f"Request came for fetching chat history of user: {user_id}")
        try:
            last_message_subquery = (
                Message.objects.filter(
                    conversation=OuterRef("pk")
                ).order_by("-created_at").values("content")[:1]
            )
            last_message_sender_subquery = (
                Message.objects.filter(
                    conversation=OuterRef("pk")
                ).order_by("-created_at").values("sender__email")[:1]
            )
            converation_list = Conversation.objects.filter(Q(user_one__id=user_id) | Q(user_two__id=user_id) | Q(group__members__id= user_id)).select_related("user_one", "user_two", "group").prefetch_related("group__members").order_by("-updated_at")
            finally_queryset = converation_list.annotate(unread_message_count=Count("messages", filter=Q(messages__is_read=False) & ~Q(messages__sender_id=user_id)), last_message=Subquery(last_message_subquery), last_message_sender=Subquery(last_message_sender_subquery))
            paginator = self.pagination_class()

            pages = paginator.paginate_queryset(finally_queryset, request)
            serialzer = self.serializer_class(pages, many=True)
            
            logger.info(f"Fetched chat history of user: {user_id}")
            return paginator.get_paginated_response(serialzer.data)
        except Exception as e:
            logger.exception(f"Error fetching chat history for user: {user_id}")
            return create_api_response(
                message="Something went wrong",
                errors={f"details: {str(e)}"},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )