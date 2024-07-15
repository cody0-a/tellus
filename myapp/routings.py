from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('chat/', consumers.ChatConsumer.as_asgi()),
    path('message/', consumers.MessageConsumer.as_asgi()),
    path('notify/', consumers.NotifyConsumer.as_asgi()),
    path('forward/', consumers.ForwardConsumer.as_asgi()),
]