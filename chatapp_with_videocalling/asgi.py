# """
# ASGI config for chatapp_with_videocalling project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp_with_videocalling.settings")

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from chatapp_with_videocalling.websocket_routing.routing import websocket_urlpatterns

# django_asgi_app = get_asgi_application()

# # from chatapp_with_videocalling.custom_middleware_websocket.token_auth_middleware import (
# #     TokenAuthMiddleware,
# # )

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": URLRouter(
#             websocket_urlpatterns
#         ),
#         # (http->django views is added by default)
#         # "websocket": TokenAuthMiddleware(
#         #     URLRouter(
#         #         # Add your WebSocket URL routing here
#         #     )
#         # ),
#     }
# )

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp_with_videocalling.settings")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp_with_videocalling.websocket_routing.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

# Now it's safe to import anything that uses Django models
from chatapp_with_videocalling.custom_middleware_websocket.token_auth_middleware import (
    TokenAuthMiddleware,
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(  # 👈 custom token middleware
            URLRouter(websocket_urlpatterns)
        ),
    }
)
