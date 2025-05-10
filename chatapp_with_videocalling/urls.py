"""
URL configuration for chatapp_with_videocalling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from chitchat.views.user_registration_views.user_registration_views import (
    UserRegistrationViewSet,
)
from chitchat.views.user_registration_views.user_email_verification_view import UserEmailVerificationView
from chitchat.views.user_registration_views.complete_user_registration import SetAccountPassword
from chitchat.views.login_views.token_obtain_view import CustomTokenObtainPairView
from chitchat.views.login_views.token_refresh_view import CustomTokenRefreshView
from rest_framework.routers import DefaultRouter
from chitchat.views.user_views.me_view import MeUserView
from chitchat.views.google_login_view.google_login_token import GoogleLoginTokenView

# Initialize the router
router = DefaultRouter()
router.register(r"register", UserRegistrationViewSet, basename="user-registration")


api_v1_routes = [
    
    # User Registration
    path("verify/<token>/email/", UserEmailVerificationView.as_view(), name="verify_email"),
    path("set-password/", SetAccountPassword.as_view(), name="complete_registration"),
    
    #Used for obtaining token and refresh token
    path("login/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh", CustomTokenRefreshView.as_view(), name="refresh_token"),
    path("google/token/", GoogleLoginTokenView.as_view(), name="google_token"),

    # Fetching current user data
    path("me/", MeUserView.as_view(), name="me_user"),
    
    #router urls
    path("", include(router.urls)),
]   

urlpatterns = [
    # Admin Site URLs
    path("admin/", admin.site.urls),
    
    # API v1 prefix routes
    path("api/v1/", include(api_v1_routes)),
    
    # Used for google login
    path('accounts/', include('allauth.urls')),
]
