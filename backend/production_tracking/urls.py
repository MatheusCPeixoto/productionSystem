from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderActivityProgressViewSet, StartActivityAppointmentView, ActivityNonConformanceViewSet


router = DefaultRouter()
router.register(r'order-activity-progress', OrderActivityProgressViewSet, basename='orderactivityprogress')
router.register(r'activity-non-conformance-log', ActivityNonConformanceViewSet, basename='activitynonconformance')

urlpatterns = [
    path('', include(router.urls)),
    path('start-activity/', StartActivityAppointmentView.as_view(), name='start-activity-api'),

]