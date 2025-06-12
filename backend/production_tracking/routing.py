# production_tracking/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),
    # Make sure this path 'ws/tasks/' matches exactly what your frontend uses.
    # The trailing slash might be important depending on your regex.
]
