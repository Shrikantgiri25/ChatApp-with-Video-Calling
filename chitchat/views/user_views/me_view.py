from rest_framework import permissions, throttling
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from chitchat.serializers.me_user_serializers import MeUserSerializer
from chitchat.utils.helpers.create_api_response import create_api_response
from rest_framework import status
from datetime import timedelta


class MeUserView(APIView):
    """
    View to update user data.
    """
    serializer_class = MeUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle]

    def get(self, request):
        """
        Get the current user's data.
        """
        print("Request user:", timedelta(days=1))
        user = request.user
        serializer = self.serializer_class(user)
        return create_api_response(
            data=serializer.data,
            message="User data retrieved successfully",
            http_status=status.HTTP_200_OK,
        )