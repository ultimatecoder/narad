from __future__ import absolute_import, unicode_literals

from django.conf import settings
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
    records_in_batch = data_frame[start_index:end_index].T.to_dict().values()
    while len(records_in_batch) != 0:
        models.Product.objects.bulk_upsert(
            conflict_target=['sku'],
            rows=records_in_batch
        )
        start_index = end_index
        end_index = end_index + settings.BATCH_SIZE_OF_PRODUCT_RECORDS
        records_in_batch = data_frame[
            start_index:end_index
        ].T.to_dict().values()

    return len(data_frame)
