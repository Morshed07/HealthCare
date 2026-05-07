from django.db import models
from apps.core.models import BaseModel
from django.utils.safestring import mark_safe


# Create your models here.


class Product(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.TextField()
    dosage_strength = models.IntegerField(help_text="The numeric value (e.g., 10, 50, 1500)")
    dosage_unit = models.CharField(
        max_length=10,
        default='mg',
        help_text="The unit of measurement (e.g., mg, mcg)"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='products/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    # information_pdf = models.FileField(upload_to='product_info_pdfs/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def image(self):
        return mark_safe('<img src="/media/%s" width = "50" height = "50" />' % (self.thumbnail))

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

        db_table = 'products'
        
        ordering = ['title']


class AdditionalDescription(BaseModel):
    product = models.ForeignKey(Product, related_name='additional_descriptions', on_delete = models.CASCADE)
    # description_title  = models.CharField(max_length=255, null=True, blank=True)
    description_content = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.description_content
    

class Pdf(BaseModel):
    product = models.ForeignKey(Product, related_name='pdfs', on_delete = models.CASCADE)
    pdf_file = models.FileField(upload_to='product_pdfs/', blank=True, null=True)
    
    def __str__(self):
        return f'File for {self.product.title}-{self.pdf_file.name}'