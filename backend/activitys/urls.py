from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ActivityViewSet


router = DefaultRouter()
router.register('activities', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]