import asyncio
import csv

from django.conf import settings

from product_manager import models


UPLOADED_FILE_NAME = settings.MEDIA_ROOT + '/products.csv'

loop = asyncio.get_event_loop()


def offload_records_to_db(file_path):
    products_to_be_created = {}
    products_to_be_updated = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = models.Product(
                sku=row['sku'],
                name=row['name'],
                description=row['description']
            )
            #if models.Product.objects.filter(sku=row['sku']).exists():
            #    products_to_be_updated[row['sku']] = product
            #else:
            #    products_to_be_created[row['sku']] = product
            products_to_be_created[row['sku']] = product
        models.Product.objects.bulk_create(
            products_to_be_created.values()
        )
        models.Product.objects.bulk_update(
            products_to_be_updated.values(),
            ['name', 'description']
        )


def products_csv_uploader(_file):
    with open(UPLOADED_FILE_NAME , 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)
    loop.run_in_executor(None, offload_records_to_db, UPLOADED_FILE_NAME)
    #offload_records_to_db(UPLOADED_FILE_NAME)
