from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Cart,
    CartItem
)


# Register your models here.

class CartAdmin(ModelAdmin):
    list_display = ("user", "subtotal", "tax_amount", "total")
    readonly_fields = ("subtotal", "tax_amount", "total")


class CartItemAdmin(ModelAdmin):
    list_display = ("cart", "product", "product_quantity", "unit_price")
    readonly_fields = ("unit_price",)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
