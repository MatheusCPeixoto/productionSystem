from rest_framework import serializers

from .models import StopReason


class StopReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopReason
        fields = '__all__'