from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.core.paginator import Paginator
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


class ProductsSearch(View):

    def get(self, request):
        form = forms.ProductSearchForm(request.GET)
        products_list = models.Product.objects.all()
        paginator = Paginator(products_list, 20)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        #form = forms.ProductSearchForm(request.POST)
        #products_list = models.Product.objects.all()
        if form.data['name']:
            products_list = products_list.filter(
                name__contains=form.data['name']
            )
        if form.data['description']:
            products_list = products_list.filter(
                description__contains=form.data['description']
            )
        if form.data['sku']:
            products_list = products_list.filter(sku=form.data['sku'])
        if form.data.get('is_active'):
            products_list = products_list.filter(is_active=True)
        else:
            products_list = products_list.filter(is_active=False)
        paginator = Paginator(products_list, 20)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(
            request,
            'product_search.html',
            {'form': form, 'products': products}
        )
        #return render(
        #    request,
        #    'product_search.html',
        #    {'form': form, 'products': products}
        #)

    def post(self, request):
        form = forms.ProductSearchForm(request.POST)
        products_list = models.Product.objects.all()
        if form.data['name']:
            products_list = products_list.filter(
                name__contains=form.data['name']
            )
        if form.data['description']:
            products_list = products_list.filter(
                description__contains=form.data['description']
            )
        if form.data['sku']:
            products_list = products_list.filter(sku=form.data['sku'])
        if form.data.get('is_active'):
            products_list = products_list.filter(is_active=True)
        else:
            products_list = products_list.filter(is_active=False)
        paginator = Paginator(products_list, 20)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(
            request,
            'product_search.html',
            {'form': form, 'products': products}
        )
