from rest_framework import serializers

from .models import Product, ProductCode, ProductFile


class ProductFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductFile
        fields = ['id', 'product', 'file_type', 'file', 'name', 'activities', 'uploaded_at']
        read_only_fields = ['file_url', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = [
            'similar_code'
        ]


class ProductSerializer(serializers.ModelSerializer):
    similar_code = ProductCodeSerializer(many=True, read_only=True, source='similar_codes')

    class Meta:
        model = Product
        fields = (
            'code',
            'product_identifier',
            'name',
            'technical_description',
            'similar_code'
        )