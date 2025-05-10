from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from chitchat.models.user_models import User
from chitchat.utils.helpers.constants import (
    USER_NOT_EXISTS,
    USER_ACCOUNT_INACTIVE,
    LOGIN_SUCCESSFUL
)
from rest_framework import status
from chitchat.utils.helpers.create_api_response import create_api_response


from django.shortcuts import redirect

class GoogleLoginTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        
        try:
            user = User.objects.get(email=email)
            
            if not user.is_active:
                return create_api_response(
                    errors=USER_ACCOUNT_INACTIVE,
                    http_status=status.HTTP_403_FORBIDDEN,
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # Send token via query param (or redirect to frontend with it)
            # frontend_redirect = GOOGLE_FRONTEND_LOGIN_REDIRECT + {access_token}
            return create_api_response(
                message=LOGIN_SUCCESSFUL,
                data={
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                    # "redirect_url": f"{GOOGLE_FRONTEND_LOGIN_REDIRECT}{access_token}"
                },
                http_status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return create_api_response(
                errors=USER_NOT_EXISTS,
                http_status=status.HTTP_404_NOT_FOUND,
            )
