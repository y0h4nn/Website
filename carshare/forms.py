from django import forms
from . import models
from django.utils.safestring import mark_safe


class AnnouncementForm(forms.ModelForm):
    prefix = 'announcement'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['id'] = "date"

    def as_p(self):
        return super().as_p() + mark_safe('''<script>
            date= document.getElementById("date");
            rome(date);
        </script>
        ''')

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


