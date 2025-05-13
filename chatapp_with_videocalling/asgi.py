"""
ASGI config for chatapp_with_videocalling project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp_with_videocalling.custom_middleware_websocket.token_auth_middleware import (
    TokenAuthMiddleware,
)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp_with_videocalling.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # (http->django views is added by default)
        "websocket": TokenAuthMiddleware(
            URLRouter(
                # Add your WebSocket URL routing here
            )
        ),
    }
)
