from django import forms
from django.contrib.auth.models import Group


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labeles = {'name': 'Nom'}
