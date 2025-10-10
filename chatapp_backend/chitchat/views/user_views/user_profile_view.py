from rest_framework import permissions, throttling, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from chitchat.models import User
from chitchat.serializers.user_profile_serializer import UserProfileSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.enums import UserStatus
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


class UserProfileView(APIView):
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
            serializer = self.serializer_class(user, context={'request': request})
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
            user_id = user.pk
            cache_key = f"user_profile_{user_id}"

            logger.info(f"[PATCH] Updating profile for: {user.email}")
            logger.info(f"[PATCH] Request data: {request.data}")
            logger.info(f"[PATCH] Request files: {request.FILES}")

            # Make mutable copy of request data
            data = request.data.copy()
            profile_data = {}

            # Handle profile_picture
            if "profile_picture" in request.FILES:
                profile_data["profile_picture"] = request.FILES["profile_picture"]
                logger.info("[PATCH] New profile picture uploaded")
            elif data.get("profile_picture") == "":
                profile_data["profile_picture"] = ""
                logger.info("[PATCH] Profile picture deletion requested")

            # Handle bio
            if "bio" in data:
                profile_data["bio"] = data.get("bio", "")
                logger.info(f"[PATCH] Bio updated: {profile_data['bio'][:50]}...")

            # Prepare final payload for serializer
            final_data = {}
            if "full_name" in data:
                final_data["full_name"] = data["full_name"]
                logger.info(f"[PATCH] Full name updated: {final_data['full_name']}")

            if profile_data:
                final_data["profile"] = profile_data

            # Automatically change NEW_USER → ACTIVE
            if user.status == "NEW_USER":
                final_data["status"] = UserStatus.ACTIVE
                logger.debug(f"[PATCH] Updating status to ACTIVE for: {user.email}")

            # Serialize with context (needed for file uploads)
            serializer = self.serializer_class(
                user,
                data=final_data,
                partial=True,
                context={"request": request},
            )

            if serializer.is_valid():
                serializer.save()
                # Clear cached profile
                cache.delete(cache_key)
                logger.info(f"[PATCH] Profile updated successfully for: {user.email}")
                return create_api_response(
                    data=serializer.data,
                    message="User data updated successfully",
                    http_status=status.HTTP_200_OK,
                )

            logger.error(f"[PATCH] Validation errors: {serializer.errors}")
            return create_api_response(
                message="Failed to update user data",
                errors=serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(f"[PATCH] Error updating profile: {e}")
            return create_api_response(
                message="An unexpected error occurred while updating user data.",
                errors={"detail": str(e)},
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
