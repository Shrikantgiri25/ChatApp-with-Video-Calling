from rest_framework import viewsets, status, permissions, throttling
from rest_framework.exceptions import Throttled
from chitchat.serializers.user_registration_serializers import (
    UserRegistrationSerializer,
)
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    EMAIL_VERIFICATION_SENT,
    USER_REGISTRATION_FAILED,
    TO_MANY_REQUEST_429,
)
from chitchat.services.email_services.email_verification_link_generator_service import (
    generate_email_verification_link,
)
from chitchat.services.email_services.send_email_verification_link import (
    send_email_verification_link,
)
from chitchat.services.user_services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def create(self, request):
        try:
            logger.info(f"Request for creating user")
            user = UserService.create_user(request.data)

            logger.info(f"Userservice created user successfully: {user.email}")
            activation_link = generate_email_verification_link(user=user)
            
            logger.info(f"Email verification link generated for user: {user.email}")
            # TODO: Add Celery for Background mail Processing with redis
            mail_sent_status = send_email_verification_link(user, activation_link)
            
            
            logger.info(f"Email sent for user: {user.email}")
            return create_api_response(
                message=EMAIL_VERIFICATION_SENT,
                data={"Email": user.email},
                http_status=status.HTTP_201_CREATED,
            )
        except Throttled as e:
            logger.error(f"Throttle limit exceeded by user: {request.data.get('email')}")
            return create_api_response(
                message=TO_MANY_REQUEST_429,
                http_status=status.HTTP_429_TOO_MANY_REQUESTS,
                errors=str(e),
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred for user: {request.data.get('email')}")
            return create_api_response(
                message=USER_REGISTRATION_FAILED,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e),
            )
