from django import forms
from . import models


class AlbumForm(forms.ModelForm):
    prefix = 'album'
    class Meta:
        model = models.Album
        fields = '__all__'
