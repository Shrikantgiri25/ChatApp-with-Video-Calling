from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import Throttled
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from chitchat.models.user_models import User
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework.status import (
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.exceptions import ValidationError
from chitchat.utils.helpers.constants import (
    USER_NOT_EXISTS,
    VERIFY_EMAIL,
    USER_ACCOUNT_INACTIVE,
    TO_MANY_REQUEST_429,
    SOMETHING_WENT_WRONG,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    return super().post(request, *args, **kwargs)
                return create_api_response(
                    message=USER_ACCOUNT_INACTIVE + " " + VERIFY_EMAIL,
                    http_status=HTTP_403_FORBIDDEN,
                )
            except User.DoesNotExist:
                raise ValidationError(USER_NOT_EXISTS)
        except Throttled as e:
            return create_api_response(
                message=TO_MANY_REQUEST_429,
                errors=str(e),
                http_status=HTTP_429_TOO_MANY_REQUESTS,
            )
        except Exception as ex:
            return create_api_response(
                message=SOMETHING_WENT_WRONG,
                errors=str(ex),
                http_status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
