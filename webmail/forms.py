from django import forms
from django.contrib.auth.models import User
from . import models

class WebmailSettingsForm(forms.ModelForm):
    prefix = "webmail"
    class Meta:
        model = models.WebmailSettings
        fields = ['webmail']
        labels = {
            'webmail': 'Webmail'
        }
