from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import OrderActivityProgressViewSet, ActivityNonConformanceViewSet

router = DefaultRouter()
router.register(r'order-activity-progress', OrderActivityProgressViewSet, basename='orderactivityprogress')
router.register(r'activity-non-conformance-log', ActivityNonConformanceViewSet, basename='activitynonconformance')

urlpatterns = [
    path('', include(router.urls)),
]