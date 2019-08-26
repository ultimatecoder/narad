from django.urls import path

from product_manager import views


app_name = 'product_manager'


urlpatterns = [
    path('products/upload/', views.upload_products, name="products-upload"),
    path(
        'products/<int:product_id>/',
        views.ProductUpdate.as_view(),
        name="product-update"
    ),
    path(
        'products/upload/progress/',
        views.ProductsUploadProgress.as_view(),
        name="products-upload-progress"
    ),
    path(
        'products/create/',
        views.ProductCreate.as_view(),
        name="product-create"
    ),
    path(
        'products/delete/',
        views.ProductsDeleteAll.as_view(),
        name="products-delete"
    ),
    path(
        'products/',
        views.ProductsSearch.as_view(),
        name="products-search"
    ),
]
