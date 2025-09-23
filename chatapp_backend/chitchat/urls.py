from django.contrib import admin
from django.urls import path, include
from chitchat.views.user_registration_views.user_registration_views import (
    UserRegistrationViewSet,
)
from chitchat.views.user_registration_views.user_email_verification_view import (
    UserEmailVerificationView,
)
from chitchat.views.user_registration_views.complete_user_registration import (
    SetAccountPassword,
)
from chitchat.views.login_views.token_obtain_view import CustomTokenObtainPairView
from chitchat.views.login_views.token_refresh_view import CustomTokenRefreshView
from rest_framework.routers import DefaultRouter
from chitchat.views.user_views.me_view import MeUserView
from chitchat.views.google_login_view.google_login_token import GoogleLoginTokenView
from chitchat.views.message_views.message_views import MessageView


# Initialize the router
router = DefaultRouter()
router.register(r"register", UserRegistrationViewSet, basename="user-registration")


api_v1_routes = [
    # User Registration
    path(
        "verify/<token>/email/",
        UserEmailVerificationView.as_view(),
        name="verify_email",
    ),
    path("set-password/", SetAccountPassword.as_view(), name="complete_registration"),
    
    # Used for obtaining token and refresh token
    path("login/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh", CustomTokenRefreshView.as_view(), name="refresh_token"),

    path("google/token/", GoogleLoginTokenView.as_view(), name="google_token"),
    # Fetching current user data
    path("profile/", MeUserView.as_view(), name="me_user"),
    # Message related views
    path("message/", MessageView.as_view(), name="message"),
    # router urls
    path("", include(router.urls)),
]