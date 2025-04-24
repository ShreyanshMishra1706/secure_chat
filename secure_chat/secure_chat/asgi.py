import os
import django

# ✅ Set DJANGO_SETTINGS_MODULE before importing anything from Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_chat.settings')

# ✅ Now initialize Django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

# ✅ ASGI application with WebSockets support
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
