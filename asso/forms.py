from django import forms
from .models import Asso


class WrapperClearableinput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '<span id="pic"><img src="%(initial_url)s" alt="photo profil" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'


class AssoForm(forms.ModelForm):
    class Meta:
        model = Asso
        fields = ['name', 'description', 'mail', 'site', 'picture']
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'mail': 'Email',
            'site': 'Site web',
            'picture': 'Image',
        }
        widgets = {
            'picture': WrapperClearableinput
        }


class AssoSettingsForm(forms.ModelForm):
    class Meta:
        model = Asso
        fields = [
            'name',
            'admins_group',
            'members_group'
        ]
        labels = {
            'name': 'Nom',
            'admins_group': 'Groupe administrateur',
            'members_group': 'Groupe des members',
        }

