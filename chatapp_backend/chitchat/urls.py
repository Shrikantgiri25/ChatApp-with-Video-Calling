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
from chitchat.views.user_views.user_profile_view import UserProfileView
from chitchat.views.google_login_view.google_login_token import GoogleLoginTokenView
from chitchat.views.message_views.message_views import MessageView
from chitchat.views.user_chat_history.user_chat_history_view import UserChatHistoryView
from chitchat.views.user_views.user_view import UserView
from chitchat.views.group_views.group_view import GroupView 
from django.conf import settings
from django.conf.urls.static import static
from chitchat.views.logout_views.logout_views import LogoutView
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
    
    # Used for obtaining login(token), logout and refresh token
    path("login/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="refresh_token"),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("google/token/", GoogleLoginTokenView.as_view(), name="google_token"),
    # Fetching current user data
    path("profile/", UserProfileView.as_view(), name="me_user"),
    # Message related views
    path("message/", MessageView.as_view(), name="message"),

    # Conversation history of User
    path("user/chats/", UserChatHistoryView.as_view(), name="message"),

    path("users/", UserView.as_view(), name="users"),

    path("group/", GroupView.as_view(), name="group"),

    # router urls
    path("", include(router.urls)),
]
if settings.DEBUG:
    api_v1_routes += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)