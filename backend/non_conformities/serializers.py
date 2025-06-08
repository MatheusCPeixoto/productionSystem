from rest_framework import serializers

from .models import NonConformance


class NonConformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonConformance
        fields = '__all__'