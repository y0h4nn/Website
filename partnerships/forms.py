from django import forms
from .models import Partnership
from django.core.files import File
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class WrapperClearableinput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '<span id="logo"><img src="%(initial_url)s" alt="logo" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'


class AddPartnershipForm(forms.ModelForm):
    class Meta :
        model = Partnership
        fields = ['logo', 'name', 'address','description', 'urlLink']

        labels = {'logo' : "Logo",
                  'name': "Nom",
                  'address' : "Adresse",
                  'description' : "Description",
                  'urlLink' : "Lien"}

        widgets = {
            'logo': WrapperClearableinput
        }

    def clean_logo(self):
        max_width = 200
        max_height = 200
        data = self.cleaned_data['logo']
        if(data):
            from django.core.files.images import get_image_dimensions
            w,h = get_image_dimensions(data)

            if(w > max_width):
                raise forms.ValidationError("La largeur de l'image doit être inferieur à  %(Value)s px", params={'Value':max_width})
            elif(h > max_height):
                raise forms.ValidationError("La hauteur de l'image doit être inferieur à  %(Value)s px", params={'Value':max_height})

        return data
