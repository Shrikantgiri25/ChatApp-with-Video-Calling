from rest_framework import viewsets, status
from chitchat.serializers.user_registration_serializers import (
    UserRegistrationSerializer,
)
from chitchat.utils.helpers.create_api_response import create_api_response
from chitchat.utils.helpers.constants import (
    USER_REGISTRATION_SUCCESSFUL,
    USER_REGISTRATION_FAILED,
)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return create_api_response(
                    message=USER_REGISTRATION_FAILED,
                    errors=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            return create_api_response(
                message=USER_REGISTRATION_SUCCESSFUL,
                data={"Id": user.id, "Email": user.email},
                http_status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return create_api_response(
                message=USER_REGISTRATION_FAILED,
                http_status=status.HTTP_400_BAD_REQUEST,
                errors=str(e),
            )
