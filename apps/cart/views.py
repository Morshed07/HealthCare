from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartUpdateSerializer,
    ApplyCouponSerializer,
    ApplyShippingCouponSerializer,
)
from .services import (
    # apply_coupon_to_cart,
    remove_coupon_from_cart,
    remove_shipping_coupon_from_cart,
)
from apps.product.models import Product


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id, in_stock=True)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            item.product_quantity += quantity
        else:
            item.product_quantity = quantity

        item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_200_OK
        )


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, item_id):
        quantity = int(request.data.get("quantity", 1))

        cart = request.user.cart
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if quantity <= 0:
            item.delete()
            return Response({"message": "Item removed"})

        item.product_quantity = quantity
        item.save()

        return Response({"message": "Cart updated"})


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = request.user.cart
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_200_OK
        )


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = request.user.cart
        cart.items.all().delete()

        return Response(
            {"message": "Cart cleared"},
            status=status.HTTP_200_OK
        )


class CartWaiverUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        cart = request.user.cart
        serializer = CartUpdateSerializer(cart, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        serializer = ApplyCouponSerializer(data=request.data)

        if serializer.is_valid():
            cart = serializer.save(cart)
            return Response(
                {
                    "message": "Coupon applied successfully",
                    "cart": CartSerializer(cart).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = request.user.cart
        remove_coupon_from_cart(cart)

        return Response(
            {
                "message": "Coupon removed successfully",
                "cart": CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )


class ApplyShippingCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        serializer = ApplyShippingCouponSerializer(
            data=request.data
        )

        if serializer.is_valid():
            cart = serializer.save(cart)
            return Response(
                {
                    "message": "Shipping coupon applied",
                    "cart": CartSerializer(cart).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RemoveShippingCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = request.user.cart
        remove_shipping_coupon_from_cart(cart)

        return Response(
            {
                "message": "Shipping coupon removed",
                "cart": CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )
