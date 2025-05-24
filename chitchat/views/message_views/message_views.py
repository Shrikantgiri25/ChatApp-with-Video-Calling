from rest_framework import permissions
from rest_framework.views import APIView

# from rest_framework.permissions import IsAuthenticated
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework import status
from chitchat.serializers.message_serializer import MessageSerializer
from chitchat.models import Message
from chitchat.models import Conversation
from chitchat.models import Group, User
from django.db.models import Q


class MessageView(APIView):
    """
    Message view to handle message-related operations.
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    # throttle_classes = [throttling.UserRateThrottle]

    def post(self, request):
        """
        Create a new message.
        """
        data = request.data
        sender = request.user.id
        group = data.get("group", None)
        reciever = data.get("receiver", None)
        if reciever:
            if not User.objects.filter(id=reciever).exists():
                return create_api_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Receiver does not exist.",
                )
            conversation, _ = Conversation.objects.get_or_create(
                Q(user_one=sender, user_two=reciever)
                | Q(user_two=sender, user_one=reciever),
                conversation_type="private",
            )
            data["conversation"] = conversation.id
        elif group:
            if not Group.objects.filter(id=group).exists():
                return create_api_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Group does not exist.",
                )
            conversation, _ = Conversation.objects.get_or_create(
                user_one=sender, group=group, conversation_type="group"
            )
            data["group"] = conversation.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return create_api_response(
            status=status.HTTP_201_CREATED,
            message="Message sent successfully",
            data=serializer.data,
        )

    def get(self, request):
        """
        Get all messages for the authenticated user.
        """
        user_one = request.user
        conversation_id = request.query_params.get("conversation_id")
        group_id = request.query_params.get("group_id")
        user_two = request.query_params.get("user_two")
        if conversation_id:
            try:
                messages = Message.objects.filter(conversation=conversation_id)
            except Conversation.DoesNotExist:
                return create_api_response(
                    status=status.HTTP_404_NOT_FOUND,
                    message="Conversation not found.",
                )
        elif group_id:
            messages = Message.objects.filter(group=group_id)
        elif user_two:
            try:
                user_two = User.objects.get(id=user_two)
            except User.DoesNotExist:
                return create_api_response(
                    status=status.HTTP_404_NOT_FOUND,
                    message="Conversation not found.",
                )
            conversation = Conversation.objects.filter(
                Q(user_one=user_one, user_two=user_two)
                | Q(user_two=user_one, user_one=user_two)
            ).first()
            if conversation:
                messages = Message.objects.filter(conversation=conversation)
            else:
                messages = []
        else:
            return create_api_response(
                status=status.HTTP_400_BAD_REQUEST,
                message="Please provide a conversation_id, group_id, or user_two.",
            )
        messages = self.serializer_class(messages, many=True).data
        return create_api_response(
            status=status.HTTP_200_OK,
            message="Messages retrieved successfully",
            data=messages,
        )
