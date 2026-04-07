from .models import CartItem, Coupon, ShippingCoupon


def add_to_cart(cart, product, quantity=1):
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.product_quantity += quantity
    else:
        item.product_quantity = quantity

    item.save()
    return item


def update_cart_item(cart_item, quantity):
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.product_quantity = quantity
        cart_item.save()


def remove_from_cart(cart_item):
    cart_item.delete()


def apply_coupon_to_cart(cart, coupon_code):
    """Apply a coupon to the cart if it's valid and active"""
    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True)
        cart.coupon = coupon
        cart.save()
        return cart, {
            "success": True,
            "message": f"Coupon '{coupon_code}' applied successfully"
        }
    except Coupon.DoesNotExist:
        return cart, {
            "success": False,
            "message": "Invalid or inactive coupon code"
        }


def remove_coupon_from_cart(cart):
    """Remove coupon from cart"""
    cart.coupon = None
    cart.save()
    return cart


def apply_shipping_coupon_to_cart(cart, coupon_code):
    """Apply a shipping coupon to the cart"""
    try:
        coupon = ShippingCoupon.objects.get(
            code=coupon_code, active=True
        )
        cart.shipping_coupon = coupon
        cart.save()
        return cart, {
            "success": True,
            "message": f"Shipping coupon '{coupon_code}' applied"
        }
    except ShippingCoupon.DoesNotExist:
        return cart, {
            "success": False,
            "message": "Invalid or inactive shipping coupon code"
        }


def remove_shipping_coupon_from_cart(cart):
    """Remove shipping coupon from cart"""
    cart.shipping_coupon = None
    cart.save()
    return cart