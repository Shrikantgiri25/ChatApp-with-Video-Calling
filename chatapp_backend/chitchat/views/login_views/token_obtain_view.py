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
    INVALID_CREDS
)
from chitchat.serializers.custom_token_obtain_serializer import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view.
    - Uses a custom serializer for token payload.
    - Adds throttling for brute-force prevention.
    - Checks if the user exists and is active before issuing tokens.
    - Handles common exceptions with consistent API responses.
    """

    # Apply both anonymous and user-specific throttling
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    # Use custom serializer for token generation (can include extra fields)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles login requests and returns JWT tokens if authentication succeeds.
        """
        try:
            email = request.data.get("email")

            # Optimization: Use `only("is_active")` to fetch only required field
            user = User.objects.filter(email=email).only("is_active").first()

            if not user:
                raise ValidationError({"detail": "Invalid credentials"}, code="unauthorized")

            if not user.is_active:
                raise ValidationError({"detail": "User inactive, verify email"}, code="forbidden")


            # If user exists and is active → proceed with normal JWT flow
            return super().post(request, *args, **kwargs)

        except Throttled as e:
            # Handles rate-limiting (too many requests)
            return create_api_response(
                success=False,
                message=TO_MANY_REQUEST_429,
                errors=str(e),
                http_status=HTTP_429_TOO_MANY_REQUESTS,
            )

        except ValidationError as ve:
            # Handles user not found (or other validation issues)
            return create_api_response(
                success=False,
                message=INVALID_CREDS,
                http_status=HTTP_403_FORBIDDEN,
            )

        except Exception as ex:
            # Handles unexpected errors gracefully
            return create_api_response(
                success=False,
                message=SOMETHING_WENT_WRONG,
                errors=str(ex),
                http_status=HTTP_500_INTERNAL_SERVER_ERROR,
            )
