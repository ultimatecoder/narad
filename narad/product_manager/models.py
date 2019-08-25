from django.db import models
from django.contrib.auth import models as user_models


class Product(models.Model):

    name = models.CharField(max_length=200, blank=None, null=None)
    sku = models.CharField(max_length=200, unique=True, blank=None, null=None)
    description = models.TextField()
    is_active = models.BooleanField(default=True)