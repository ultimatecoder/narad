from channels.routing import ProtocolTypeRouter, URLRouter
from product_manager import routing


application = ProtocolTypeRouter({
    'http': URLRouter(routing.urlpatterns),
})
