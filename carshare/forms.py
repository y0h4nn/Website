from django import forms
from . import models
from django.utils.safestring import mark_safe


class AnnouncementForm(forms.ModelForm):
    prefix = 'announcement'
    date = forms.SplitDateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['id'] = "date"

    def as_p(self):
        return super().as_p() + mark_safe('''<script>
            create_calendar("date_0")
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
            'price',
            'description',
        ]

        labels = {
            'title': 'Titre',
            'source': 'Lieu de départ',
            'destination': 'Lieu d\'arrivé',
            'places': 'Nombre de places',
            'price': 'Prix',
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


