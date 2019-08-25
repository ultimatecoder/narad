from django.contrib import admin

from product_manager import models


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Product, ProductAdmin)
