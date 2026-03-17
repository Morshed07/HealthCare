from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    additional_descriptions = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "short_description",
            "dosage_strength",
            "dosage_unit",
            "price",
            "thumbnail",
            "quantity",
            "in_stock",
            "information_pdf",
            'additional_descriptions',
            "created_at",
            "updated_at"
        ]

        read_only_fields = ("id", "created_at", "updated_at")
        
    def get_additional_descriptions(self, obj):
        descriptions = obj.additional_descriptions.all()
        return [
            {
                # In the provided code snippet, `"description_title": desc.description_title` is
                # creating a key-value pair in a dictionary.
                # "description_title": desc.description_title,
                "description_content": desc.description_content
            }
            for desc in descriptions
        ]