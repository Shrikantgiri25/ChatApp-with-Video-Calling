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
from chitchat.views.user_registration_views.user_activation_view import ActivateUserView
from chitchat.views.login_views.token_obtain_view import CustomTokenObtainPairView
from chitchat.views.login_views.token_refresh_view import CustomTokenRefreshView
from rest_framework.routers import DefaultRouter

# Initialize the router
router = DefaultRouter()
router.register(r"register", UserRegistrationViewSet, basename="user-registration")

urlpatterns = [
    path("activate/<token>/user/", ActivateUserView.as_view(), name="activate_user"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Used for obtaining token and refresh token
    path("api/token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh", CustomTokenRefreshView.as_view(), name="refresh_token"),

    # Used for google login
    path('accounts/', include('allauth.urls')),
]
