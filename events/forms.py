from django.forms import ModelForm, SplitDateTimeField, ClearableFileInput
from .models import Event

class WrapperClearableinput(ClearableFileInput):
    template_with_initial = (
        '<span id="pic"><img src="%(initial_url)s" alt="event photo" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'


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
        widgets = {'photo': WrapperClearableinput}

