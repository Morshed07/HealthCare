from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Cart,
    CartItem,
    Coupon
)


# Register your models here.

class CartAdmin(ModelAdmin):
    list_display = ("user", "subtotal", "tax_amount", "total")
    readonly_fields = ("subtotal", "tax_amount", "total")


class CartItemAdmin(ModelAdmin):
    list_display = ("cart", "product", "product_quantity", "unit_price")
    readonly_fields = ("unit_price",)


class CouponAdmin(ModelAdmin):
    list_display = ("code", "discount_amount", "active")
    list_filter = ("active",)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon, CouponAdmin)

