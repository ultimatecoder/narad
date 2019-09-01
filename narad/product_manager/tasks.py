from __future__ import absolute_import, unicode_literals
from celery import shared_task

from product_manager import models


@shared_task(name="upload_products_as_csv_file")
def upload_products_as_csv_file(object_pk):
    file_object = models.ProductsAsCsvFile.objects.get(object_pk)
    print(file_object.uploaded_at)
    print("==="* 12)
    return 4
