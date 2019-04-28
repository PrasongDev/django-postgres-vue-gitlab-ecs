import jwt

from channels.auth import AuthMiddlewareStack, CookieMiddleware
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        cookies = scope['cookies']
        if 'user-token' in cookies:
            token = jwt.decode(
                cookies['user-token'],
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_id = token['user_id']
            try:
                user = User.objects.get(id=user_id)
                scope['user'] = user
            except User.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: CookieMiddleware(TokenAuthMiddleware(AuthMiddlewareStack(inner))) # noqa