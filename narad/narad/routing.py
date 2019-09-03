from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from product_manager import routing


application = ProtocolTypeRouter({
    'http': AuthMiddlewareStack(
        URLRouter(
            routing.urlpatterns
        )
    ),
})
