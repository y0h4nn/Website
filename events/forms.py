from django.forms import ModelForm, ClearableFileInput, SplitDateTimeField, IntegerField
from django.utils.safestring import mark_safe
from .models import Event, ExternInscription, ExternLink, Invitation, RecurrentEvent


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
            create_calendar("id_end_inscriptions_0")
            create_calendar("id_start_time_0")
            create_calendar("id_end_time_0")
            create_calendar("id_invitations_start_0")
        </script>
        ''')

    start_time = SplitDateTimeField(label="Début")
    end_time = SplitDateTimeField(label="Fin")
    end_inscriptions = SplitDateTimeField(label="Fin des inscriptions")
    invitations_start = SplitDateTimeField(label="Début des invitations", required=False)
    class Meta:
        model = Event
        exclude = ["uuid"]
        labels = {'name': "Nom", 'location': "Lieu", 'private': "Privé",
                  'allow_extern': "Autoriser les exterieurs", 'limited': "Nombre d'inscriptions limité",
                  'max_inscriptions': "Nombre maximum d'inscriptions", 'allow_invitations': "Autoriser les invitations",
                  'max_invitations': "Nombre maximum d'invitations", 'max_invitations_by_person': "Nombre maximum d'invitations par personne"}
        widgets = {'photo': WrapperClearableinput,}


class RecurrentEventForm(EventForm):
    delay = IntegerField()
    class Meta(EventForm.Meta):
        model = RecurrentEvent
        exclude = ["uuid", "last_created"]



class ExternInscriptionForm(ModelForm):
    class Meta:
        model = ExternInscription
        labels = {'first_name': "Prénom", 'last_name': "Nom", 'birth_date': "Date de naissance"}
        exclude = ["event", "via", "in_date"]


class ExternLinkForm(ModelForm):
    class Meta:
        model = ExternLink
        labels = {"name": "Pour", "maximum": "Nombre de places"}
        fields = ["name", "maximum"]


class InvitForm(ModelForm):
    class Meta:
        model = Invitation
        labels = {'first_name': "Prénom", 'last_name': "Nom", 'birth_date': "Date de naissance"}
        fields = ["mail", "birth_date", "first_name", "last_name"]

