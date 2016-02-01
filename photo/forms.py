from django import forms
from . import models


class AccessPolicyForm(forms.ModelForm):
    class Meta:
        model = models.AccessPolicy
        exclude = ['path']


class PublicAccessForm(AccessPolicyForm):
    """ Accès publique """
    class Meta:
        model = models.PublicAccess
        exclude = ['path']


class GroupAccessForm(AccessPolicyForm):
    """ Accès pour un groupe donné """
    class Meta:
        model = models.GroupAccess
        fields = ['group']


class EventAccessForm(AccessPolicyForm):
    """ Accès aux participants d'un évènement donné """
    class Meta:
        model = models.EventAccess
        fields = ['event']


def get_forms():
    return {c.__name__: c for c in AccessPolicyForm.__subclasses__()}

