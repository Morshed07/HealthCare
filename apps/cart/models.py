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
    def tax_amount(self):
        return (self.subtotal * self.tax_percentage) / Decimal("100")

    @property
    def total(self):
        return self.subtotal + self.tax_amount

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
