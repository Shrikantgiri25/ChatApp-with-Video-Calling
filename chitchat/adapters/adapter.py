from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token  # or use JWT
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)  # or JWT generation
        frontend_url = "http://localhost:8000/api/v1/google/token/"  # e.g., "http://localhost:3000"
        # return f"{frontend_url}/?token={token.key}"
        return frontend_url