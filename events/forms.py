from django.forms import ModelForm, ClearableFileInput
from django.utils.safestring import mark_safe
from .models import Event, ExternInscription

class WrapperClearableinput(ClearableFileInput):
    template_with_initial = (
        '<span id="pic"><img src="%(initial_url)s" alt="event photo" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'


class EventForm(ModelForm):
    def clean(self):
        super().clean()
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        end_ins = self.cleaned_data.get('end_inscriptions')

        if start is None or end is None or end_ins is None:
            return

        if end <= start:
            self.add_error('start_time', "Le début de l'événement doit se situer avant sa fin...")
        if end_ins > start:
            self.add_error('end_inscriptions', "La fin des inscriptions doit se situer avant le début de l'évènement")

    def as_p(self):
        return super().as_p() + mark_safe('''<script>
            start = document.getElementById("id_start_time");
            end = document.getElementById("id_end_time");
            end_ins = document.getElementById("id_end_inscriptions");
            rome(start, {dateValidator: rome.val.beforeEq(end)});
            rome(end_ins, {dateValidator: rome.val.beforeEq(start)});
            rome(end, {dateValidator: rome.val.afterEq(start)});
        </script>
        ''')

    class Meta:
        model = Event
        exclude = ["uuid"]
        labels = {'name': "Nom", 'start_time': "Début", 'end_time': "Fin",
                  'location': "Lieu", 'private': "Privé", 'end_inscriptions': "Fin des inscriptions",
                  'allow_extern': "Autoriser les exterieurs", 'max_extern': "Nombre maximum d'éxterieurs"}
        widgets = {'photo': WrapperClearableinput}


class ExternInscriptionForm(ModelForm):
    class Meta:
        model = ExternInscription
        labels = {'first_name': "Prénom", 'last_name': "Nom"}
        exclude = ["event"]

