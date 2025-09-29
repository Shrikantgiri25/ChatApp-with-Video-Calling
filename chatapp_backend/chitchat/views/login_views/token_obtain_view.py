from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import Throttled, AuthenticationFailed
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework.status import (
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from chitchat.utils.helpers.constants import (
    TO_MANY_REQUEST_429,
    SOMETHING_WENT_WRONG,
)
from chitchat.serializers.custom_token_obtain_serializer import CustomTokenObtainPairSerializer
import logging

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)

        except Throttled as e:
            logger.error(f"Too many login attempts: {request.data.get('email')} - {str(e.detail)}")
            return create_api_response(
                success=False,
                message=TO_MANY_REQUEST_429,
                errors=str(e),
                http_status=HTTP_429_TOO_MANY_REQUESTS,
            )
        except AuthenticationFailed as ve:
            logger.error(f"Authentication Failed: {request.data.get('email')} - {str(ve.detail)}")
            return create_api_response(
                success=False,
                message=ve.detail,
                errors=ve.detail,
                http_status=HTTP_401_UNAUTHORIZED,
            )
        except Exception as ex:
            logger.error(f"Unexpected error for user: {request.data.get('email')} - {str(ex)}")
            return create_api_response(
                success=False,
                message=SOMETHING_WENT_WRONG,
                errors=str(ex),
                http_status=HTTP_500_INTERNAL_SERVER_ERROR,
            )