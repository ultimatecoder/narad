from django.urls import path

from product_manager import views, models

app_name = 'product_manager'


urlpatterns = [
    path(
        'products/upload/',
        views.ProductsAsCsvFileCreateView.as_view(),
        name="products-upload"
    ),
    path(
        'products/<str:product_id>/',
        views.ProductUpdate.as_view(),
        name="product-update"
    ),
    path(
        'products/upload/progress/<str:task_id>',
        views.ProductsUploadProgress.as_view(),
        name="products-upload-progress"
    ),
    path(
        'products-create/',
        views.ProductCreate.as_view(),
        name="product-create"
    ),
    path(
        'products-delete/',
        views.ProductsDeleteAll.as_view(),
        name="products-delete"
    ),
    path(
        'products/',
        views.ProductsSearch.as_view(),
        name="products-search"
    ),
    path(
        '',
        views.Home.as_view(),
        name="index"
    )
]
