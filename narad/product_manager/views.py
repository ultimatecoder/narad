from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from product_manager import forms, models
from .handlers import products_csv_uploader


def upload_products(request):
    if request.method == 'POST':
        form = forms.ProductUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            products_csv_uploader(request.FILES['file'])
            return HttpResponseRedirect('/products')
    else:
        form = forms.ProductUploaderForm()
        return render(request, 'upload.html', {'form': form})


class ProductUpdate(View):

    def get(self, request, product_id):
        try:
            product = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            raise Http404("Product does not exist")
        form = forms.ProductForm(instance=product)
        return render(request, 'product_detail.html', {
            'form': form, 'product_id': product_id
        })

    def post(self, request, product_id):
        try:
            product = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            raise Http404("Product does not exist")
        form = forms.ProductForm(request.POST, instance=product)
        form.save()
        return HttpResponseRedirect('/products')


class ProductCreate(View):

    def get(self, request):
        form = forms.ProductForm()
        return render(request, 'product_create.html', {'form': form })

    def post(self, request):
        form = forms.ProductForm(request.POST)
        form.save()
        return HttpResponseRedirect('/products')


class ProductsDeleteAll(View):

    def get(self, request):
        models.Product.objects.all().delete()
        return HttpResponseRedirect(reverse('products-upload'))
