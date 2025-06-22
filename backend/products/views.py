from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('similar_codes').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset = ProductFilter

