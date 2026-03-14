from rest_framework import serializers
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem, OrderStatusHistory
from apps.cart.models import Cart


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["status", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "crosscheck_id",
            "product",
            "product_title",
            "quantity",
            "price",
            "dosage_strength",
            "dosage_unit",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)
    order_history = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "facility_name",
            "contact_person",
            "email",
            "mobile_number",
            "address",
            "city",
            "state",
            "zip_code",
            "payment_method",
            "shipping_charge",
            "sub_total",
            "total",
            "tax_amount",
            "status",
            'created_at',
            'updated_at',
            "orderitems",
            "order_history"
        ]
        read_only_fields = (
            "order_id",
            "user",
            "sub_total",
            "total",
            "status",
            "paid",
            'created_at'
        )

    def get_order_history(self, obj):
        history = obj.status_history.all()
        return OrderHistorySerializer(history, many=True).data


class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "facility_name",
            "contact_person",
            "email",
            "mobile_number",
            "address",
            "city",
            "state",
            "zip_code",
            "payment_method",
            "shipping_charge",
        ]

    def validate(self, attrs):
        user = self.context["request"].user

        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found")

        if cart.items.count() == 0:
            raise serializers.ValidationError("Cart is empty")

        if not cart.liability_waiver_accepted:
            raise serializers.ValidationError(
                "You must accept the liability waiver before checkout."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        cart = user.cart

        # --------- CALCULATE FROM CART ---------
        subtotal = cart.subtotal
        tax = cart.tax_amount
        total = cart.total + validated_data.get("shipping_charge", Decimal("0.00"))

        # --------- CREATE ORDER ---------
        order = Order.objects.create(
            user=user,
            sub_total=subtotal,
            total=total,
            tax_amount=tax,
            **validated_data
        )

        # --------- COPY CART ITEMS ---------
        for item in cart.items.select_related("product"):

            product = item.product

            # Optional stock check
            if product.quantity < item.quantity:
                raise serializers.ValidationError(
                    f"{product.title} is out of stock"
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price,  # lock price
                dosage_strength=product.dosage_strength,
                dosage_unit=product.dosage_unit,
            )

            # Deduct stock
            product.quantity -= item.quantity
            if product.quantity == 0:
                product.in_stock = False
            product.save()

        # --------- CLEAR CART ---------
        cart.items.all().delete()
        cart.liability_waiver_accepted = False
        cart.save()

        return order