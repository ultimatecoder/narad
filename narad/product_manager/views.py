import asyncio
from threading import Thread

from celery.result import AsyncResult
from django.http import QueryDict
from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from product_manager import forms, models, tasks


class ProductsAsCsvFileCreateView(CreateView):

    model = models.ProductsAsCsvFile
    fields = ['upload', ]

    def form_valid(self, form, *args, **kwargs):
        redirect_url = super(
            ProductsAsCsvFileCreateView, self
        ).form_valid(form)
        return redirect_url

    def get_success_url(self):
        task_id = tasks.upload_products_as_csv_file.delay(self.object.pk)
        return reverse_lazy(
            'products-upload-progress', kwargs={'task_id': task_id}
        )


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
        try:
            page = request.GET['page']
            request_data = request.GET.copy()
            del request_data['page']
        except KeyError:
            page = None
            request_data = request.GET
        if request_data == {}:
            form = forms.ProductSearchForm()
            form_first_load = True
            search_query_string = ''
        else:
            form_first_load = False
            form = forms.ProductSearchForm(request_data)
            search_query_string = form.data.urlencode()
        products_list = models.Product.objects.all()
        if form.data.get('name'):
            products_list = products_list.filter(
                name__contains=form.data['name']
            )
        if form.data.get('description'):
            products_list = products_list.filter(
                description__contains=form.data['description']
            )
        if form.data.get('sku'):
            products_list = products_list.filter(sku=form.data['sku'])
        if (form.data.get('is_active') == 'on') or (form_first_load):
            products_list = products_list.filter(is_active=True)
        else:
            products_list = products_list.filter(is_active=False)
        paginator = Paginator(products_list, 20)
        products = paginator.get_page(page)
        return render(
            request,
            'product_search.html',
            {
                'form': form,
                'products': products,
                'search_query_string': search_query_string
            }
        )


class ProductsUploadProgress(View):

    def get(self, request, task_id):
        task = AsyncResult(task_id)
        return render(
            request,
            'products_upload_progress.html',
            {'task_id': task_id}
        )


class Home(View):

    def get(self, request):
        return HttpResponseRedirect(reverse('products-search'))
