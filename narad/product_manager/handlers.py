import asyncio
import csv
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
    products_to_be_created = {}
    products_to_be_updated = {}
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
            #if models.Product.objects.filter(sku=row['sku']).exists():
            #    products_to_be_updated[row['sku']] = product
            #else:
            #    products_to_be_created[row['sku']] = product
            products_to_be_created[row['sku']] = product
        new_products = len(products_to_be_created)

        send_event('test', 'message', f"Found {new_products} to be created")
        models.Product.objects.bulk_create(
            products_to_be_created.values()
        )
        send_event(
            'test',
            'message',
            f"Uploaded {new_products} products successfully!"
        )
        models.Product.objects.bulk_update(
            products_to_be_updated.values(),
            ['name', 'description']
        )
    send_event("test", "message", "uploading completed")


def products_csv_uploader(_file):
    file_name = generate_new_csv_file_name()
    file_path = f"{settings.MEDIA_ROOT}/{file_name}"

    with open(file_path , 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)
    loop.run_in_executor(None, offload_records_to_db, file_path)
