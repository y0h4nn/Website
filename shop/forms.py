from django import forms
from . import models


class ProductForm(forms.ModelForm):
    prefix = 'product'
    class Meta:
        model = models.Product
        fields = [
            'name',
            'price',
            'description',
            'action',
            'event',
        ]

        labels = {
            'name': 'Nom',
            'price': 'Prix',
            'description': 'Description',
            'action': 'Action additionelle',
            'event': 'Inscription à l\'evenement',
        }


class PackForm(forms.ModelForm):
    prefix = 'pack'
    class Meta:
        model = models.Packs
        fields = [
            'name',
            'price',
            'description',
            'products',
        ]

        labels = {
            'name': 'Nom',
            'price': 'Prix',
            'description': 'Description',
            'products': 'Produit',
        }

        widgets = {
            'products': forms.CheckboxSelectMultiple,
        }
