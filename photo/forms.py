from django import forms
from . import models


class AccessPolicyForm(forms.ModelForm):
    class Meta:
        model = models.AccessPolicy
        exclude = ['path']


class PublicAccessForm(AccessPolicyForm):
    """ Access publique """
    class Meta:
        model = models.PublicAccess
        exclude = ['path']

class GroupAccessForm(AccessPolicyForm):
    """ Access pour un groupe donné """
    class Meta:
        model = models.GroupAccess
        fields = ['group']


class EventAccessForm(AccessPolicyForm):
    """ Access au participants d'un evenement donné """
    class Meta:
        model = models.EventAccess
        fields = ['event']


def get_forms():
    return {c.__name__: c for c in AccessPolicyForm.__subclasses__()}

