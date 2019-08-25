from django.urls import path

from product_manager import views


app_name = 'product_manager'


urlpatterns = [
    path('products/upload/', views.upload_products, name="products-upload")
]
