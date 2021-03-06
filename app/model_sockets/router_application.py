from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing as model_sockets_router


def flatten(l):
    flat = []
    for sublist in l:
        for item in sublist:
            flat.append(item)
    return flat


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                flatten([
                    model_sockets_router.websocket_urlpatterns,
                ])
            )
        ),
    )
})
