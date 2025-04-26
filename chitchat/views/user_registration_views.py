from rest_framework import viewsets, status, permissions, throttling
from rest_framework.exceptions import Throttled
from chitchat.serializers.user_registration_serializers import (
    UserRegistrationSerializer,
)
from rest_framework.views import APIView
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    EMAIL_VERIFICATION_SENT,
    USER_REGISTRATION_FAILED,
    TO_MANY_REQUEST_429,
    EMAIL_VERIFICATION_FAILED,
    EMAIL_VERIFICATION_SUCCESSFUL,
    SOMETHING_WENT_WRONG,
)
from chitchat.services.email_services.email_verification_link_generator_service import (
    generate_email_verification_link,
)
from chitchat.services.email_services.send_email_verification_link import (
    send_email_verification_link,
)
from chitchat.services.user_services.user_service import UserService
from chitchat.services.email_services.email_verifying_token_verification_service import (
    verify_user_email_verification_token,
)
from rest_framework.exceptions import ValidationError


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def create(self, request):
        try:
            user = UserService.create_user(request.data)
            activation_link = generate_email_verification_link(user=user)
            mail_sent_status = send_email_verification_link(user, activation_link)
            return create_api_response(
                message=EMAIL_VERIFICATION_SENT,
                data={"Email": user.email},
                http_status=status.HTTP_201_CREATED,
            )
        except Throttled as e:
            return create_api_response(
                message=TO_MANY_REQUEST_429,
                http_status=status.HTTP_429_TOO_MANY_REQUESTS,
                errors=str(e),
            )
        except Exception as e:
            return create_api_response(
                message=USER_REGISTRATION_FAILED,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )


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
                http_status=status.HTTP_202_ACCEPTED,
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
