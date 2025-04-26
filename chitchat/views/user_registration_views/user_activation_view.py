from rest_framework import status, permissions
from rest_framework.views import APIView
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    EMAIL_VERIFICATION_FAILED,
    EMAIL_VERIFICATION_SUCCESSFUL,
    SOMETHING_WENT_WRONG,
)

from chitchat.services.email_services.email_verifying_token_verification_service import (
    verify_user_email_verification_token,
)
from rest_framework.exceptions import ValidationError


class ActivateUserView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            user_data = verify_user_email_verification_token(token=token)
            user_data.is_active = True
            user_data.save()
            return create_api_response(
                data={"Email": user_data.email},
                message=EMAIL_VERIFICATION_SUCCESSFUL,
                http_status=status.HTTP_204_NO_CONTENT,
            )
        except ValidationError as e:
            return create_api_response(
                message=EMAIL_VERIFICATION_FAILED,
                errors=str(e),
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return create_api_response(
                message=SOMETHING_WENT_WRONG,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )
