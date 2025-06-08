from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, BranchViewSet


router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'branches', BranchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]