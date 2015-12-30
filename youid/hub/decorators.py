import functools
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authtoken.models import Token
from channels.decorators import channel_session, http_session

def authenticate_credentials(self, key):
    try:
        token = Token.objects.select_related('user').get(key=key)
    except Token.DoesNotExist:
        raise exceptions.AuthenticationFailed(_('Invalid token.'))

    if not token.user.is_active:
        raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

    return (token.user, token)


def http_token_user(func):
    """
    Wraps a HTTP or WebSocket consumer (or any consumer of messages
    that provides a "COOKIES" attribute) to provide both a "session"
    attribute and a "user" attibute, like AuthMiddleware does.
    This runs http_session() to get a session to hook auth off of.
    If the user does not have a session cookie set, both "session"
    and "user" will be None.
    """
    @http_session
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # If we didn't get a session, then we don't get a user
        print message.content, message.channel
        if not hasattr(message, "http_session"):
            raise ValueError("Did not see a http session to get auth from")
        if message.http_session is None:
            message.user = None
        # Otherwise, be a bit naughty and make a fake Request with just
        # a "session" attribute (later on, perhaps refactor contrib.auth to
        # pass around session rather than request)
        else:
            fake_request = type("FakeRequest", (object, ), {"session": message.http_session})
            message.user = auth.get_user(fake_request)
        # Run the consumer
        return func(message, *args, **kwargs)
    return inner