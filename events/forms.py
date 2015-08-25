from django.forms import ModelForm, TextInput, ClearableFileInput, ValidationError
from django.utils.safestring import mark_safe
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
        self.fields['start_time'].widget.attrs['id'] = 'start_time'
        self.fields['end_time'].widget.attrs['id'] = 'end_time'

    def clean_end_time(self):
        start = self.cleaned_data['start_time']
        end = self.cleaned_data['end_time']

        if end <= start:
            raise ValidationError("Le début de l'événement doit se situer avant sa fin...")

        return end

    def as_p(self):
        return super().as_p() + mark_safe('''<script>
            start = document.getElementById("start_time");
            end = document.getElementById("end_time");
            rome(start);
            rome(end, {dateValidator: rome.val.afterEq(start)});
        </script>
        ''')

    class Meta:
        model = Event
        fields = "__all__"
        labels = {'name': "Nom", 'start_time': "Début", 'end_time': "Fin", 'location': "Lieu"}
        widgets = {'photo': WrapperClearableinput}

