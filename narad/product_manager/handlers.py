import asyncio
import csv
import json
import os
import uuid

from django.conf import settings
from django.core import serializers
from django.db import transaction
from django_eventstream import send_event
import redis

from product_manager import models


asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()


def generate_new_csv_file_name():
    file_id = uuid.uuid4()
    return f"{file_id}.csv"


def offload_records_to_db(file_path):
    _redis = redis.from_url(settings.REDISGO_URL, charset="utf-8")
    send_event('test', 'message', "Document uploaded successfully!")
    batch_size = 200000000000
    products_to_be_created = []
    products_to_be_updated = []
    unique_id = uuid.uuid4()

    with _redis.pipeline() as pipeline:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            send_event('test', 'message', f"Processing uploaded file...")
            for row in reader:
                serialized_product = json.dumps({
                    'name': row['name'],
                    'description': row['description']
                })
                _redis.hset(str(unique_id), row['sku'], serialized_product)
        pipeline.execute()
    products_to_be_updated = []
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    with _redis.pipeline() as pipeline:
        for existing_product in models.Product.objects.filter(
            sku__in=map(lambda k: k.decode(), _redis.hkeys(str(unique_id)))
        ):
            product_fields_in_json = _redis.hget(
                str(unique_id), existing_product.pk
            )
            product_fields = json.loads(product_fields_in_json)
            _redis.hdel(str(unique_id), existing_product.pk)
            if (
                (product_fields['name'] != existing_product.name) or
                (product_fields['description'] != existing_product.description)
            ):
                existing_product.name = product_fields['name']
                existing_product.description = product_fields['description']
                products_to_be_updated.append(existing_product)
                if len(products_to_be_updated) == batch_size:
                    models.Product.objects.bulk_update(
                        products_to_be_updated,
                        fields=['name', 'description'],
                        batch_size=batch_size
                    )
                    products_to_be_updated = []
        if products_to_be_updated:
            models.Product.objects.bulk_update(
                products_to_be_updated,
                fields=['name', 'description'],
                batch_size=batch_size
            )
            products_to_be_updated = []
        pipeline.execute()
    products_to_be_created = []
    with _redis.pipeline() as pipeline:
        for sku, fields_in_json in _redis.hscan_iter(str(unique_id)):
            fields = json.loads(fields_in_json)
            product = models.Product(
                sku=sku.decode(),
                name=fields['name'],
                description=fields['description']
            )
            _redis.hdel(str(unique_id), sku)
            products_to_be_created.append(product)
            if len(products_to_be_created) == batch_size:
                models.Product.objects.bulk_create(
                    products_to_be_created, batch_size
                )
                products_to_be_created = []
        if products_to_be_created:
            models.Product.objects.bulk_create(
                products_to_be_created, batch_size
            )
            products_to_be_created = []
        pipeline.execute()
    send_event("test", "message", "uploading completed")
    os.remove(file_path)


def products_csv_uploader(_file):
    file_name = generate_new_csv_file_name()
    file_path = f"{settings.MEDIA_ROOT}/{file_name}"

    with open(file_path , 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)
    loop.run_in_executor(None, offload_records_to_db, file_path)
