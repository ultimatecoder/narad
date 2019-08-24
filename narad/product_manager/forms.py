from django import forms


class ProductUploaderForm(forms.Form):
    file = forms.FileField()
