from django import forms
from . import models


class AnnouncementForm(forms.ModelForm):
    prefix = 'announcement'

    class Meta:
        model = models.Announcement
        fields = [
            'title',
            'source',
            'destination',
            'date',
            'places',
            'description',
        ]

        labels = {
            'title': 'Titre',
            'source': 'Lieux de départ',
            'destination': 'Lieux d\'arrivé',
            'places': 'Nombre de places',
        }


class RegistrationForm(forms.ModelForm):
    prefix = "registration"
    class Meta:
        model = models.Registration
        fields = [
            'comment',
        ]
        labels = {
            'comment': 'Demande',
        }


