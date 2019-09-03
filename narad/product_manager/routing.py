from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack

from . import consumers


urlpatterns = [
    url(r"^events/(?P<task_id>.+)/$", consumers.ServerSentEventsConsumer),
    url(r'', AsgiHandler),
]
