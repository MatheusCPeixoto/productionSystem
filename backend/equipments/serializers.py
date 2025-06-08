from rest_framework import serializers

from .models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = '__all__'

    def get_description(self, obj):
        original_description = obj.description
        if not original_description or not isinstance(original_description, str):
            return original_description
        return original_description.title()