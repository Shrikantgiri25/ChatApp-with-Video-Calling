from rest_framework import permissions, throttling, status
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from chitchat.models import User
from chitchat.serializers.userlist_serializer import UserListSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.enums import UserStatus
from chitchat.utils.helpers.pagination import Pagination
from rest_framework import filters
import logging

logger = logging.getLogger(__name__)


class UserView(APIView):
    """
    View to retrieve and update user data.
    """

    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    pagination_class = Pagination
    def get(self, request):
        try:
            query_params = request.query_params.get("search", "")
            user_id = request.user.pk
            all_userlist = User.objects.filter(email__icontains=query_params).exclude(Q(id=user_id) | Q(status__in=[UserStatus.INACTIVE, UserStatus.NOT_VERIFIED])).select_related("profile").only("id", "email", "status", "profile__profile_picture", "profile__bio")
            paginator = self.pagination_class()
            pages = paginator.paginate_queryset(all_userlist, request)
            serializer = self.serializer_class(pages, many=True)
            logger.info(f"Fetched all users for: {user_id}")
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            logger.exception(f"[GET] Unexpected error for fetching userlist: {request.user.email}: {e}")
            return create_api_response(
                message="An unexpected error occurred while fetching user data.",
                errors={"detail": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )