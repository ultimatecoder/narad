import asyncio
import csv
import os
import uuid

from django.conf import settings
from django_eventstream import send_event

from product_manager import models


asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()


def generate_new_csv_file_name():
    file_id = uuid.uuid4()
    return f"{file_id}.csv"


def offload_records_to_db(file_path):
    products = {}
    send_event('test', 'message', "Document uploaded successfully!")
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        send_event('test', 'message', f"Processing uploaded file")
        for row in reader:
            product = models.Product(
                sku=row['sku'],
                name=row['name'],
                description=row['description']
            )
            products[row['sku']] = product
        existing_products = models.Product.objects.filter(
            sku__in=products.keys()
        )
        products_to_be_updated = []
        for existing_product in existing_products:
            product = products[existing_product.pk]
            del products[existing_product.pk]
            if (
                (product.name != existing_product.name) or
                (product.description != existing_product.description)
            ):
                existing_product.name = product.name
                existing_product.description = product.description
                products_to_be_updated.append(existing_product)
        new_products = len(products)
        send_event('test', 'message', f"Found {new_products} new products...")
        models.Product.objects.bulk_create(
            products.values(),
            ignore_conflicts=True
        )
        existing_products = len(products_to_be_updated)
        send_event(
            'test',
            'message',
            f"Found {existing_products} existing products to be updated..."
        )
        models.Product.objects.bulk_update(
            products_to_be_updated,
            ['name', 'description']
        )
        send_event(
            'test',
            'message',
            "Uploaded products successfully!"
        )
    send_event("test", "message", "uploading completed")
    os.remove(file_path)


def products_csv_uploader(_file):
    file_name = generate_new_csv_file_name()
    file_path = f"{settings.MEDIA_ROOT}/{file_name}"

    with open(file_path , 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)
    loop.run_in_executor(None, offload_records_to_db, file_path)
