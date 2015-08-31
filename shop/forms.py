from django import forms
from . import models


class ProductForm(forms.ModelForm):
    prefix = 'product'
    class Meta:
        model = models.Product
        fields = [
            'name',
            'price',
            'action',
        ]

        labels = {
            'name': 'Nom',
            'price': 'prix',
            'action': 'Action additionelle',
        }

