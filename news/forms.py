from django import forms
from . import models


class NewsForm(forms.ModelForm):
    prefix = 'news'

    class Meta:
        model = models.News
        fields = [
            'title',
            'content',
        ]

        labels = {
            'title': 'Titre',
            'content': 'contenu',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', ]
        labels = {'content': 'Commentaire'}
