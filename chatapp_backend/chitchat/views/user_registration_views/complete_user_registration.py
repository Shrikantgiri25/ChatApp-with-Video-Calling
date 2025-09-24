import logging
from rest_framework.views import APIView
from rest_framework import status, permissions, throttling
from rest_framework.exceptions import Throttled

from chitchat.serializers.user_serializer import UserSerializer
from chitchat.services.user_services.user_service import UserService
from chitchat.services.token_services.verify_decode_token import verify_decode_token
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    USER_ACCOUNT_CREATED,
    TO_MANY_REQUEST_429,
    SOMETHING_WENT_WRONG,
    SET_PASSWORD,
)
from chitchat.utils.helpers.enums import UserStatus

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Use DEBUG for more detailed logs

class SetAccountPassword(APIView):
    """
    View to update user data.
    """

    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def post(self, request):
        logger.info("SetAccountPassword POST request received")
        try:
            data = request.data.copy()
            token = data.pop("token_id", None)

            if not token:
                logger.warning("Token not provided in request")
                return create_api_response(
                    message="Token is required",
                    http_status=status.HTTP_400_BAD_REQUEST,
                )

            # Verify the token and get the user email
            token_data = verify_decode_token(token_id=token, purpose=SET_PASSWORD)
            user_email = token_data["email"]
            logger.info(f"Token verified for email: {user_email}")

            data["email"] = user_email
            user = UserService.update_user(data=data)
            logger.info(f"User account updated for email: {user.email}")

            return create_api_response(
                message=USER_ACCOUNT_CREATED,
                data={"Email": user.email},
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
            logger.exception(f"Unexpected error in SetAccountPassword: {e}")
            return create_api_response(
                message=SOMETHING_WENT_WRONG,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )
