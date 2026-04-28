from django.db import models
from apps.core.models import BaseModel
from apps.product.models import Product
# Create your models here.


class Service(BaseModel):
    title = models.CharField(max_length=200, help_text="Service title")
    description = models.TextField(help_text="Service description")
    products = models.ManyToManyField(
        Product,
        related_name="services",
        help_text="Products associated with this service",
        blank=True
    )

    def __str__(self):
        return self.title
