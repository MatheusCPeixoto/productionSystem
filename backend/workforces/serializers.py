from rest_framework import serializers

from .models import Workforce


class WorkforceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Workforce
        fields = '__all__'

    def get_name(self, obj):
        original_name = obj.name
        if not original_name or not isinstance(original_name, str):
            return original_name
        return original_name.title()