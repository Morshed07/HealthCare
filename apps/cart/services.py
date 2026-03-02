from .models import CartItem


def add_to_cart(cart, product, quantity=1):
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    item.save()
    return item


def update_cart_item(cart_item, quantity):
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()


def remove_from_cart(cart_item):
    cart_item.delete()