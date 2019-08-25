from django import forms

from product_manager import models


class ProductUploaderForm(forms.Form):
    file = forms.FileField()


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ["name", "description", "sku", "is_active"]
