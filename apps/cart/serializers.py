from rest_framework import serializers
from .models import Cart, CartItem, Coupon
from apps.product.models import Product


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["id", "code", "discount_amount", "active"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "short_description",
            "dosage_strength",
            "dosage_unit",
            "thumbnail",
            "quantity"
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_quantity",
            "unit_price",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    coupon_discount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    tax_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "subtotal",
            "coupon",
            "coupon_discount",
            "tax_percentage",
            "tax_amount",
            "total",
            "total_items",
            "liability_waiver_accepted"
        ]


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "liability_waiver_accepted"
        ]


class ApplyCouponSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(max_length=50, required=True)

    def validate_coupon_code(self, value):
        try:
            coupon = Coupon.objects.get(code=value, active=True)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive coupon code")
        return coupon

    def save(self, cart):
        coupon = self.validated_data['coupon_code']
        cart.coupon = coupon
        cart.save()
        return cart
