from django.urls import path, include
from rest_framework import routers

from .views import WorkforceViewSet

router = routers.DefaultRouter()
router.register(r'workforce', WorkforceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]