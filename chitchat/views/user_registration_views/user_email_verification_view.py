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
    SET_PASSWORD
)

from chitchat.services.token_services.verify_decode_token import (
    verify_decode_token,
)
from chitchat.services.token_services.token_generator_service import generate_token
from rest_framework.exceptions import ValidationError
from chitchat.utils.helpers.enums import UserStatus
from chitchat.models.user_models import User


class UserEmailVerificationView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            token = verify_decode_token(token=token, purpose=USER_EMAIL_VERIFICATION)
            user_email = token["email"]
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                raise ValidationError(USER_NOT_EXISTS)

            if user.status == UserStatus.VERIFIED:
                raise ValidationError(LINK_EXPIRED)
            else:
                user.status = UserStatus.VERIFIED
                user.save()
                token = generate_token(user=user, purpose=SET_PASSWORD, lifetime=10) #10 minutes
            return create_api_response(
                data={"Email": user_email, "token": str(token)},
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
