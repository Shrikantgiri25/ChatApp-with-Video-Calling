from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import Throttled
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework.status import (
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Throttled as e:
            return create_api_response(
                errors=str(e), http_status=HTTP_429_TOO_MANY_REQUESTS
            )
        except Exception as ex:
            return create_api_response(
                errors=str(ex), http_status=HTTP_500_INTERNAL_SERVER_ERROR
            )
