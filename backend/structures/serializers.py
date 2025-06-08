from rest_framework import serializers

from .models import StructureActivity
from activitys.serializers import ActivitySerializer


class StructureActivitySerializer(serializers.ModelSerializer):
    activity_description = serializers.CharField(source='activity_code.description', read_only=True)

    class Meta:
        model = StructureActivity
        fields = (
            'code',
            'sequence',
            'activity_code',
            'activity_description'
        )