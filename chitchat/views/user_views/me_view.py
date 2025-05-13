from rest_framework import permissions, throttling
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from chitchat.serializers.me_user_serializers import MeUserSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework import status
from datetime import timedelta
from chitchat.utils.helpers.enums import UserStatus
from rest_framework.parsers import MultiPartParser, FormParser


class MeUserView(APIView):
    """
    View to update user data.
    """

    serializer_class = MeUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Get the current user's data.
        """
        user = request.user
        serializer = self.serializer_class(user)
        return create_api_response(
            data=serializer.data,
            message="User data retrieved successfully",
            http_status=status.HTTP_200_OK,
        )

    def patch(self, request):
        """
        Update the current user's data.
        """
        user = request.user
        data = request.data
        print("data", data)
        if user.status == "NEW_USER":
            data["status"] = UserStatus.ACTIVE
        if user.status == "INACTIVE":
            return create_api_response(
                message="User account is inactive.",
                errors={"status": "User account is inactive."},
                http_status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return create_api_response(
                data=serializer.data,
                message="User data updated successfully",
                http_status=status.HTTP_200_OK,
            )

        return create_api_response(
            message="Failed to update user data",
            errors=serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )
