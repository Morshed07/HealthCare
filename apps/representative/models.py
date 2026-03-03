from django.db import models
from apps.core.models import BaseModel
from django.utils.safestring import mark_safe

# Create your models here.


class Representative(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(upload_to='representatives/avatars/', blank=True, null=True)
    company = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    representative_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Representative"
        verbose_name_plural = "Representatives"
        db_table = "representatives"
        ordering = ["-created_at"]
        
        indexes = [
            # 1. Fast lookup for the unique representative code
            models.Index(fields=["representative_code"]),

            # 2. Case-insensitive search or prefix search for companies
            models.Index(fields=["company"]),

            # 3. Composite Index: Highly useful for dashboard/admin lists
            # where you filter for "Active" representatives sorted by "Created Date"
            models.Index(fields=["is_active", "-created_at"]),
        ]

        db_table = "representatives"
        ordering = ["-created_at"]

    def picture(self):
        return mark_safe('<img src="/media/%s" width = "80" height = "80" />' % (self.avatar))