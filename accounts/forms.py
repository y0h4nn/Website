from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from . import models


class WrapperClearableinput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '<span id="pic"><img src="%(initial_url)s" alt="photo profil" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'


class UserForm(forms.ModelForm):
    prefix = 'user'
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']


class ProfileForm(forms.ModelForm):
    prefix = 'profile'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthdate'].widget.attrs['id'] = 'birth_date'

    def as_p(self):
        return super().as_p() + mark_safe('''<script>
            bd = document.getElementById("birth_date");
            rome(bd, {time: false});
        </script>
        ''')

    class Meta:
        model = models.Profile
        fields = [
            'nickname',
            'phone',
            'birthdate',
            'family',
            'promo',
            'enib_join_year',
            'semester'
        ]

        labels = {
            'nickname': 'Surnom',
            'picture': 'Image de profil',
            'phone': 'Téléphone',
            'birthdate': 'Date de naissance',
            'family': 'Famille',
            'promo': 'Promo',
            'enib_join_year': 'Date d\'inscription à l\'enib',
            'semester': 'Semestre'
        }


class ImageProfileForm(forms.ModelForm):
    prefix = "profile_img"
    class Meta:
        model = models.Profile
        fields = [
            'picture',
        ]

        labels = {
            'picture': 'Image de profil',
        }

        widgets = {
            'picture': WrapperClearableinput
        }

class AddressForm(forms.ModelForm):
    prefix = "address"
    class Meta:
        model = models.Address
        fields = [
            'street',
            'postal_code',
            'town',
        ]
        labels = {
            'street': 'voie',
            'postal_code': 'Code postal',
            'town': 'Ville',
        }

