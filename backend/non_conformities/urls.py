from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NonConformanceViewSet


router = DefaultRouter()
router.register(r'non-conformance', NonConformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
