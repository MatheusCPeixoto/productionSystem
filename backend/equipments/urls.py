from django.urls import path, include
from rest_framework import routers

from .views import EquipmentViewSet

router = routers.DefaultRouter()
router.register(r'equipments', EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]