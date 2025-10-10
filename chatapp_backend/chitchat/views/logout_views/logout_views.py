from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from chitchat.utils.helpers.create_api_response import create_api_response
import logging

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return create_api_response(
                    success=False,
                    message="Refresh token is required.",
                    errors={"refresh": "Missing refresh token."},
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.email} successfully logged out.")
            return create_api_response(
                success=True,
                message="Logout successful.",
                http_status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError as e:
            logger.warning(f"Invalid or expired token for user {request.user.email}: {str(e)}")
            return create_api_response(
                success=False,
                message="Invalid or expired token.",
                errors=str(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as ex:
            logger.error(f"Unexpected logout error for {request.user.email}: {str(ex)}")
            return create_api_response(
                success=False,
                message="Something went wrong during logout.",
                errors=str(ex),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
