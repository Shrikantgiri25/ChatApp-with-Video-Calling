# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from chitchat.utils.helpers.constants import USER_ACCOUNT_INACTIVE, INVALID_CREDS

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"  # Use email for authentication

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Authenticate using email
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError({"detail": INVALID_CREDS})

        if not user.is_active:
            raise serializers.ValidationError({"detail": f"{USER_ACCOUNT_INACTIVE}. Please verify your email."})

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
