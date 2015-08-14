from django.forms import ModelForm, SplitDateTimeField
from .models import Event


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f, label in {'start_time': "Début", 'end_time': "Fin"}.items():
            self.fields[f] = SplitDateTimeField(label=label)
            self.fields[f].widget.widgets[0].attrs['placeholder'] = "DD/MM/YYYY"
            self.fields[f].widget.widgets[1].attrs['placeholder'] = "HH:MM"

    class Meta:
        model = Event
        fields = "__all__"
        labels = {'name': "Nom", 'start_time': "Début", 'end_time': "Fin", 'location': "Lieu"}

