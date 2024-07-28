import os
import django
from channels.routing import get_default_application, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from myproject.consumers import ChatConsumer, ItemConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/', ChatConsumer.as_asgi()),
            path('ws/items/', ItemConsumer.as_asgi()),
        ])
    ),
})

