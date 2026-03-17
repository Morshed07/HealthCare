from django.conf import settings
from django.db import models
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from apps.core.models import BaseModel
from apps.product.models import Product


class Cart(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("09.25")
    )
    coupon = models.ForeignKey(
        'Coupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts"
    )
    liability_waiver_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} Cart- liability_waiver_accepted {self.liability_waiver_accepted}"

    # --------- CALCULATIONS ----------

    @property
    def subtotal(self):
        result = self.items.aggregate(
            total=Sum(
                F("product_quantity") * F("product__price"),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
        return result["total"] or Decimal("0.00")

    @property
    def coupon_discount(self):
        if self.coupon and self.coupon.active:
            return self.coupon.discount_amount
        return Decimal("0.00")

    @property
    def tax_amount(self):
        # Calculate tax on subtotal minus coupon discount
        taxable_amount = self.subtotal - self.coupon_discount
        return (taxable_amount * self.tax_percentage) / Decimal("100")

    @property
    def total(self):
        return self.subtotal - self.coupon_discount + self.tax_amount

    @property
    def total_items(self):
        return self.items.aggregate(
            total=Sum("product_quantity")
        )["total"] or 0


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    product_quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.title} x {self.product_quantity}"

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.product_quantity


class Coupon(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code