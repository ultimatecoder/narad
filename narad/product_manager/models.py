from django.db import models
from psqlextra.models import PostgresModel


class Product(PostgresModel):

    name = models.CharField(max_length=200, blank=None, null=None)
    sku = models.CharField(
        max_length=200, unique=True, blank=None, null=None, primary_key=True
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class ProductsAsCsvFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
