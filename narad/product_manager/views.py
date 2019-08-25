from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ProductUploaderForm
from .handlers import products_csv_uploader


def upload_products(request):
    if request.method == 'POST':
        form = ProductUploaderForm(request.POST, request.FILES)
        if form.is_valid():
            products_csv_uploader(request.FILES['file'])
            return HttpResponseRedirect('/products')
    else:
        form = ProductUploaderForm()
        return render(request, 'upload.html', {'form': form})
