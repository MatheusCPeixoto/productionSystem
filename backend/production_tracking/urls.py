from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import OrderActivityProgressViewSet, ActivityNonConformanceViewSet, ActivityEquipmentLogViewSet, ActivityWorkforceLogViewSet

router = DefaultRouter()
router.register(r'order-activity-progress', OrderActivityProgressViewSet, basename='orderactivityprogress')
router.register(r'activity-non-conformance-log', ActivityNonConformanceViewSet, basename='activitynonconformance')
router.register(r'activity-equipment-log', ActivityEquipmentLogViewSet, basename='activityequipmentlog')
router.register(r'activity-workforce-log', ActivityWorkforceLogViewSet, basename='activityworkforcelog')


urlpatterns = [
    path('', include(router.urls)),
]