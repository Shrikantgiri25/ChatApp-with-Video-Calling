from channels.middleware import BaseMiddleware

# from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from chitchat.models.user_models import User


class TokenAuthMiddleware(BaseMiddleware):
    """Middleware to authenticate WebSocket connections using JWT tokens."""

    @database_sync_to_async
    def getUser(self, token):
        # User = get_user_model()
        return User.objects.get(id=token["user_id"])

    async def __call__(self, scope, receive, send):
        from urllib.parse import parse_qs
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth.models import AnonymousUser

        query_string = scope.get("query_string").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        if token:
            try:
                # Import User model inside the function to avoid "Apps aren't loaded yet" error
                access_token = AccessToken(token)

                user = await self.getUser(access_token)
                scope["user"] = user
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
