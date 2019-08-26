from django import forms

from product_manager import models


class ProductUploaderForm(forms.Form):
    file = forms.FileField()


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ["name", "description", "sku", "is_active"]


#class ProductSearchForm(forms.Form):
#    name = forms.CharField(max_length=200, required=False)
#    description = forms.CharField(required=False, widget=forms.Textarea)
#    sku = forms.CharField(max_length=200, required=False)
#    is_active = forms.BooleanField(required=False)


class ProductSearchForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    sku = forms.CharField(max_length=200, required=False)
    #is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = models.Product
        fields = ["name", "description", "sku", "is_active"]
