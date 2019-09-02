from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db.models import Q
import pandas

from narad.celery import app
from product_manager import models


@app.task
def upload_products_as_csv_file(uploaded_file_pk):
    file_object = models.ProductsAsCsvFile.objects.get(
        pk=uploaded_file_pk
    )
    data_frame = pandas.read_csv(file_object.upload.file)
    data_frame.drop_duplicates("sku", keep='last', inplace=True)
    end_index = settings.BATCH_SIZE_OF_PRODUCT_RECORDS
    start_index = 0
    records_in_batch = data_frame[start_index:end_index]
    while len(records_in_batch) != 0:
        records = []
        for index, values in records_in_batch.iterrows():
            records.append(
                models.Product(
                    pk=values['sku'],
                    name=values['name'],
                    description=values['description']
                )
            )
        models.Product.objects.bulk_update(records, ['name', 'description'])
        models.Product.objects.bulk_create(records, ignore_conflicts=True)
        start_index = end_index
        end_index = end_index + settings.BATCH_SIZE_OF_PRODUCT_RECORDS
        records_in_batch = data_frame[start_index:end_index]
    return len(data_frame)
