# your_project_name/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # If you need authentication
import production_tracking.routing  # Assuming your routing is in production_tracking/routing.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # Or just URLRouter if no auth needed yet
        URLRouter(
            production_tracking.routing.websocket_urlpatterns
        )
    ),
})
