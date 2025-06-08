from django.urls import path, include
from rest_framework import routers

from .views import StopReasonViewSet

router = routers.DefaultRouter()
router.register(r'stop-reason', StopReasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]