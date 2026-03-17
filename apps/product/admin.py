from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Product, AdditionalDescription


class AdditionalDescriptionInline(TabularInline):
    model = AdditionalDescription
    extra = 1
    fields = ("description_content", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


class ProductAdmin(ModelAdmin):
    list_display = (
        "title",
        "image",
        "dosage_strength",
        "dosage_unit",
        "price",
        "quantity",
        "in_stock",
        "created_at",
    )
    search_fields = ("title", "slug")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10
    prepopulated_fields = {"slug": ("title",)}

    inlines = [AdditionalDescriptionInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "thumbnail",
                    "short_description",
                    "dosage_strength",
                    "dosage_unit",
                    "price",
                    "quantity",
                    "information_pdf",
                    "in_stock",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


admin.site.register(Product, ProductAdmin)