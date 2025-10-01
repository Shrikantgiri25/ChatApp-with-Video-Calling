from rest_framework import permissions, throttling, status
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from chitchat.models import User
from chitchat.serializers.user_profile_serializer import UserProfileSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.enums import UserStatus
import logging

logger = logging.getLogger(__name__)


class UserProfileView(APIView):
    """
    View to retrieve and update user data.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    parser_classes = [MultiPartParser, FormParser] 
    def get(self, request):
        user_id = request.user.pk
        cache_key = f"user_profile_{user_id}"
        user_profile = cache.get(cache_key)
        if user_profile:
            return create_api_response(
                data=user_profile,
                message="User data retrieved successfully",
                http_status=status.HTTP_200_OK,
            )
        try:
            logger.info(f"[GET] Request for user profile: {request.user.email}")
            user = (
                User.objects.select_related("profile")
                .only(
                    "id",
                    "email",
                    "full_name",
                    "status",
                    "profile__profile_picture",
                    "profile__bio",
                    "profile__is_online",
                    "profile__last_seen",
                )
                .get(pk=request.user.pk)
            )
            serializer = self.serializer_class(user)
            logger.info(f"[GET] Fetched profile successfully for: {user.email}")
            user_data = serializer.data
            cache.set(key=cache_key, value=user_data, timeout=60 * 15)
            return create_api_response(
                data=user_data,
                message="User data retrieved successfully",
                http_status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            logger.error(f"[GET] User not found: {request.user.email}")
            return create_api_response(
                message="User not found.",
                errors={"user": "No user exists with the provided credentials."},
                http_status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception(f"[GET] Unexpected error for user {request.user.email}: {e}")
            return create_api_response(
                message="An unexpected error occurred while fetching user data.",
                errors={"detail": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request):
        try:
            user = request.user
            logger.info(f"[PATCH] Request for updating user profile: {user.email}")

            if user.status == "INACTIVE":
                logger.warning(f"[PATCH] Inactive user attempted update: {user.email}")
                return create_api_response(
                    message="User account is inactive.",
                    errors={"status": "User account is inactive."},
                    http_status=status.HTTP_403_FORBIDDEN,
                )

            # Make a mutable copy of request.data
            data = request.data.copy()

            # Automatically activate NEW_USER
            if user.status == "NEW_USER":
                logger.debug(f"[PATCH] Updating status to ACTIVE for: {user.email}")
                data["status"] = UserStatus.ACTIVE

            serializer = self.serializer_class(user, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                logger.info(f"[PATCH] Profile updated successfully for: {user.email}")
                return create_api_response(
                    data=serializer.data,
                    message="User data updated successfully",
                    http_status=status.HTTP_200_OK,
                )

            # If serializer validation fails
            logger.error(f"[PATCH] Validation errors for {user.email}: {serializer.errors}")
            return create_api_response(
                message="Failed to update user data",
                errors=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(f"[PATCH] Unexpected error for user {user.email}: {e}")
            return create_api_response(
                message="An unexpected error occurred while updating user data.",
                errors={"detail": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
