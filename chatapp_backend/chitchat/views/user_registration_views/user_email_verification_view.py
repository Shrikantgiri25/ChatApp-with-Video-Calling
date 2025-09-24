import logging
from rest_framework import status, permissions
from rest_framework.views import APIView
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    EMAIL_VERIFICATION_FAILED,
    EMAIL_VERIFICATION_SUCCESSFUL,
    SOMETHING_WENT_WRONG,
    USER_NOT_EXISTS,
    USER_EMAIL_VERIFICATION,
    LINK_EXPIRED,
    SET_PASSWORD,
)
from chitchat.services.token_services.verify_decode_token import verify_decode_token
from chitchat.services.token_services.token_generator_service import generate_token
from rest_framework.exceptions import ValidationError
from chitchat.utils.helpers.enums import UserStatus
from chitchat.models.user_models import User

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # or DEBUG for more details

class UserEmailVerificationView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        logger.info("Starting email verification process")
        try:
            token_data = verify_decode_token(token_id=token, purpose=USER_EMAIL_VERIFICATION)
            user_email = token_data["email"]
            logger.info(f"Decoded token for email: {user_email}")

            try:
                user = User.objects.only("email", "status").get(email=user_email)
            except User.DoesNotExist:
                logger.warning(f"User not found for email: {user_email}")
                raise ValidationError(USER_NOT_EXISTS)

            if user.status == UserStatus.VERIFIED:
                logger.info(f"User {user_email} already verified")
                raise ValidationError(LINK_EXPIRED)
            else:
                user.status = UserStatus.VERIFIED
                user.save(update_fields=["status"])
                logger.info(f"User {user_email} status updated to VERIFIED")

                token = generate_token(
                    user=user, purpose=SET_PASSWORD, lifetime=10
                )
                logger.info(f"Generated set-password token for user {user_email}")

            return create_api_response(
                data={"Email": user_email, "token_id": token.id},
                message=EMAIL_VERIFICATION_SUCCESSFUL,
                http_status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(f"Validation error during email verification: {e}")
            return create_api_response(
                message=EMAIL_VERIFICATION_FAILED,
                errors=str(e),
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.exception(f"Unexpected error during email verification: {e}")
            return create_api_response(
                message=SOMETHING_WENT_WRONG,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )
