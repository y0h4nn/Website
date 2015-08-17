from django import forms
from . import models


class AddContributorForm(forms.ModelForm):
    prefix = 'contributor'
    class Meta:
        model = models.Contributor
        fields = '__all__'
